import numpy as np
import spacy
import regex as re


class InteractionsCounter:

    def __init__(self, narrator: str = None):
        self.prev_matrix: np.ndarray = np.zeros((1, 1))
        self.prev_characters: list[str] = []
        self.character_dict: dict[str, [str]] = {} if not narrator else {"I": [narrator]}
        self.first_interactions_overall: dict = {}
        self.first_interactions_per_char: dict = {}
        self.first_person: bool = narrator is not None

    def _get_characters(self, doc) -> list[str]:
        all_characters = sorted(
            set(self.prev_characters +
                [ent.text.title().replace("_", "").removesuffix("'S") for ent in doc.ents if ent.label_ == "PERSON"]))
        return sorted(self._pool_characters(all_characters))

    def _setup_interactions(self, characters: list[str]) -> dict[str, dict[str, float]]:
        interactions = {character: {character2: 0.0 for character2 in characters}
                        for character in characters}
        for i in range(len(self.prev_characters)):
            for j in range(i + 1, len(self.prev_characters)):
                char1, char2 = self.prev_characters[i], self.prev_characters[j]
                for c1_full_name in self.character_dict[char1]:
                    for c2_full_name in self.character_dict[char2]:
                        interactions[c1_full_name][c2_full_name] = self.prev_matrix[i][j]
                        interactions[c2_full_name][c1_full_name] = self.prev_matrix[j][i]
        return interactions

    def _pool_characters(self, all_characters: list[str]) -> list[str]:
        character_matches = {ch: [ch2 for ch2 in all_characters if ch == ch2 or ch in re.split(" |-", ch2)] for ch in
                             all_characters}
        # Reduce to disjoint characters
        for (ch, names) in character_matches.items():
            for name1 in names:
                for name2 in names:
                    if name2 != name1 and name2 in name1:
                        names.remove(name2)
        for name in character_matches:
            # full_name = str(max(character_matches[name], key=len)) if character_matches[name] else name
            self.character_dict[name] = character_matches[name]

        return list(set([name for full_names in self.character_dict.values() for name in full_names]))

    def _update_interactions_records(self, interactions: dict, sentence: str, first_char: str, second_char: str):
        # If first char not in dict, add to dict
        if self.first_interactions_per_char.get(first_char) is None:
            self.first_interactions_per_char[first_char] = {}
        # If they have not interacted before
        if self.first_interactions_per_char.get(first_char).get(second_char) is None:
            self.first_interactions_per_char[first_char].update({second_char: sentence})
        # If this is their first overall interaction
        if not sum(interactions[first_char].values()):
            self.first_interactions_overall[first_char] = {"with": second_char, "context": sentence}
        if second_char in interactions and not sum(interactions[second_char].values()):
            self.first_interactions_overall[second_char] = {"with": first_char, "context": sentence}

    def update_interactions(self, p1, p2, interactions, text):
        for first_char in self.character_dict[p1]:
            for second_char in self.character_dict[p2]:
                if first_char == second_char:
                    continue
                self._update_interactions_records(interactions, text, first_char, second_char)
                # Increment interactions
                interactions[first_char][second_char] += 1
                interactions[second_char][first_char] += 1

    def generate_interactions_matrix(self, text: str) -> tuple[np.ndarray, list[str]]:
        try:
            nlp = spacy.load("en_core_web_lg")
        except OSError:
            spacy.cli.download("en_core_web_lg")
            nlp = spacy.load("en_core_web_lg")

        doc = nlp(text)
        characters = self._get_characters(doc)
        interactions = self._setup_interactions(characters)

        for sentence in doc.sents:
            people = list(dict.fromkeys(
                [ent.text.title().replace("_", "").removesuffix("'S") for ent in sentence.ents if
                 ent.label_ == "PERSON"]))
            pronouns = list(set([pn.text.title() for pn in sentence if pn.pos_ == "PRON" and pn.text == "I"]))
            if self.first_person:
                people.extend(pronouns)
            for i in range(len(people)):
                for j in range(i + 1, len(people)):
                    # Track first interactions
                    self.update_interactions(people[i], people[j], interactions, text)

        interactions_matrix = np.zeros((len(characters), len(characters)))

        for (i, char_interactions) in enumerate(interactions.values()):
            for (j, num_interactions) in enumerate(char_interactions.values()):
                interactions_matrix[i][j] = num_interactions
        self.prev_matrix = interactions_matrix
        self.prev_characters = characters
        return interactions_matrix, characters

    def __call__(self, text: str) -> tuple[np.ndarray, list[str]]:
        return self.generate_interactions_matrix(text)

    def get_metadata(self) -> dict:
        return {
            "first interactions overall": dict.copy(self.first_interactions_overall),
            "first interactions per char": dict.copy(self.first_interactions_per_char)
        }
