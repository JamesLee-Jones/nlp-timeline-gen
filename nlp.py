import numpy as np
import spacy
import json
import sys


def process_data(text, chapter_regex):
    # TODO: Determine and justify this value (currently a dummy value)
    NUM_SPLITS = 10
    """
    :param text: The full text to be analysed.
    :param chapter_regex: Regex by which chapters are determined. If chapter_regex=="", split into equal length sections.
    :return: Returns list of sections
    """
    if chapter_regex:
        timeline = text.split(chapter_regex)
    else:
        # TODO: Figure out sensible split that preserves semantics of text i.e. by paragraph
        paragraphs = text.split("\n")
        num_sections = min(NUM_SPLITS, len(paragraphs))
        per_section = len(paragraphs) // NUM_SPLITS
        k, m = divmod(len(paragraphs), NUM_SPLITS)
        # This combines paragraphs into NUM_SPLIT sections and then restores the paragraph structure
        timeline = ["\n".join(paragraphs[i * k + min(i, m): (i + 1) * k + min(i + 1, m)]) for i in range(num_sections)]
    cleaned_data = []
    for segment in timeline:
        segment = segment.rstrip()
        segment = segment.replace("\n", " ")
        segment = segment.replace("\r", " ")
        cleaned_data.append(segment)
    return cleaned_data


def generate_interactions_matrix(text, prev_matrix, prev_characters):
    try:
        nlp = spacy.load("en_core_web_md")
    except OSError:
        spacy.cli.download("en_core_web_md")
        nlp = spacy.load("en_core_web_md")

    doc = nlp(text)

    characters = list(set(prev_characters + [ent.text for ent in doc.ents if ent.label_ == "PERSON"]))
    characters.sort()
    interactions = {character: {character2: 0.0 for character2 in characters}
                    for character in characters}

    for i in range(len(prev_characters)):
        for j in range(i + 1, len(prev_characters)):
            char1, char2 = prev_characters[i], prev_characters[j]
            interactions[char1][char2] = prev_matrix[i][j]
            interactions[char2][char1] = prev_matrix[j][i]
    for sentence in doc.sents:
        people = list(dict.fromkeys(
            [ent.text for ent in sentence.ents if ent.label_ == "PERSON"]))
        for i in range(len(people)):
            for j in range(i + 1, len(people)):
                interactions[people[i]][people[j]] += 1
                interactions[people[j]][people[i]] += 1

    interactions_matrix = np.zeros((len(characters), len(characters)))
    norm_interactions_matrix = np.zeros((len(characters), len(characters)))

    for (i, char_interactions) in enumerate(interactions.values()):
        row_sum = sum(char_interactions.values())
        for (j, num_interactions) in enumerate(char_interactions.values()):
            interactions_matrix[i][j] = num_interactions
            norm_interactions_matrix[i][j] = num_interactions / row_sum if row_sum != 0 else 0
    return norm_interactions_matrix, interactions_matrix, characters


def generate_timeline_json(sections, title):
    interactions = []
    characters = []
    json_contents = {"book": title,
                     "num_sections": len(sections),
                     "sections": []
                     }
    for section in sections:
        normalised_interactions, interactions, characters = generate_interactions_matrix(section, interactions,
                                                                                         characters)
        json_contents["sections"].append({
            "names": characters,
            "matrix": normalised_interactions.tolist()
        })
    with open("{}_analysis.json".format(title), "w", newline='\r\n') as f:
        f.write(json.dumps(json_contents, indent=2))


# TODO: Implement main function so script can be called from CLI
def main():
    pass


if __name__ == '__main__':
    pass

# sections = ["Harry and Sally went to the park.", "At the park, Harry saw John.", "John then called Margaret to join them."]
# title = "example"
# generate_timeline_json(sections, title)
