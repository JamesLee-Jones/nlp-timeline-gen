import React, {useEffect, useState, useRef} from "react";
import "./App.css";
import {ForceGraph2D} from "react-force-graph";
import * as d3 from "d3";

function HomePage() {

    const buttons = [
        {id: 0, title: "I"},
        {id: 1, title: "II"},
        {id: 2, title: "III"},
        {id: 3, title: "IV"},
        {id: 4, title: "V"}
    ];

    const [selected, setSelected] = useState(0);
    const [state, setState] = useState({
        color: "blue"
    });

    const handleColor = (row) => {
        setSelected(row.id);
    };

    const selectLeft = (row_id) => {
        setSelected(((row_id - 1) + 5) % 5);
    }

    const selectRight = (row_id) => {
        setSelected((row_id + 1) % 5);
    }

    useEffect(() => {
        document.body.style.backgroundColor = "#F5EEE2";
    });

    let node = [
        {id: "id1", name: "Harry", val: "3"},
        {id: "id2", name: "Ron", val: "3"},
        {id: "id3", name: "Hermione", val: "3"},
        {id: "id4", name: "Dumbledore", val: "3"},
        {id: "id5", name: "Snape", val: "3"},
        {id: "id6", name: "Dobby", val: "3"},
        {id: "id7", name: "Draco", val: "3"},
        {id: "id8", name: "Neville", val: "3"},

    ];

    let link = [
        {source: "id1", target: "id4"},
        {source: "id2", target: "id3"},
        {source: "id2", target: "id4"},
        {source: "id3", target: "id4"},
        {source: "id4", target: "id5"},
        {source: "id4", target: "id6"},
        {source: "id4", target: "id7"},
        {source: "id5", target: "id8"},
    ];

    const width = 1000;
    const height = 800;

    const homePageGraph = useRef();

    useEffect(() => {
        homePageGraph.current.d3Force("charge", d3.forceManyBody().strength(-100));
        homePageGraph.current.d3Force("center", d3.forceCenter(0, 0));
        homePageGraph.current.d3Force("collide", d3.forceCollide());
        homePageGraph.current.d3Force("y", d3.forceY(-10));
        homePageGraph.current.d3Force("x", d3.forceX(-10));
        homePageGraph.current.zoom(6);
        homePageGraph.current.centerAt(homePageGraph.current.d3Force());
    }, []);

    return (
        <>
    <main className="container" id="chronolog-header" role="main">
                <div className="row justify-content-start">
                    <div className="col-4">
                        <div className="row">
                                <img src="../ChronoLogoTransparent.png" className="img-fluid" alt="ChronoLogo"/>
                        </div>
                        <div className="row"><p className="home-para">Bring literature to life with ChronoLog's book visualizations.</p></div>
                        <div className="row">

                        </div>
                    </div>
                    <div className="col-8 homeGraph"><ForceGraph2D
                        graphData={{nodes: node, links: link}}
                        nodeLabel="name"
                        linkWidth={4}
                        linkDirectionalParticleWidth={4}
                        nodeAutoColorBy={"name"}
                        width={width}
                        height={height}
                        ref={homePageGraph}
                        enablePanInteraction={true}
                        enableZoomInteraction={true}
                    /></div>
                </div>
    </main>
            {/*<div className="container">*/}
            {/*    <div className="row text-center">*/}
            {/*        <div className="col-sm text-center">*/}
            {/*            <Button style={{backgroundColor: "#22333b"}}>*/}
            {/*                <KeyboardArrowLeft style={{color: "#eae0d5"}} onClick={() => selectLeft(selected)}/>*/}
            {/*            </Button>*/}
            {/*        </div>*/}
            {/*        {buttons.map((list) => (*/}
            {/*            <div className="col-sm text-center">*/}
            {/*                <IconButton>*/}
            {/*                    <CircleIcon variant="outlined"*/}
            {/*                                id={list.id}*/}
            {/*                                onClick={() => handleColor(list)}*/}
            {/*                                style={{*/}
            {/*                                    color: list.id === selected ? "#22333b" : "#eae0d5",*/}
            {/*                                    borderColor: list.id === selected ? "#22333b" : "#eae0d5"*/}
            {/*                                }}>*/}
            {/*                    </CircleIcon>*/}
            {/*                </IconButton>*/}
            {/*            </div>*/}

            {/*        ))}*/}
            {/*        <div className="col-sm text-center">*/}
            {/*            <Button style={{backgroundColor: "#22333b"}}>*/}
            {/*                <KeyboardArrowRight style={{color: "#eae0d5"}} onClick={() => selectRight(selected)}/>*/}
            {/*            </Button>*/}
            {/*        </div>*/}
            {/*    </div>*/}
            {/*    <div className="row text-center">*/}
            {/*        <div className="col-sm">*/}
            {/*        </div>*/}
            {/*        {buttons.map((list) => (*/}
            {/*            <div className="col-sm text-center">*/}
            {/*                <Typography>*/}
            {/*                    {list.title}*/}
            {/*                </Typography>*/}

            {/*            </div>*/}

            {/*        ))}*/}
            {/*        <div className="col-sm">*/}
            {/*        </div>*/}
            {/*    </div>*/}
            {/*</div>*/}

        </>

    );

}

export default HomePage;
