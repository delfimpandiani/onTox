## Use Cases

In this section, we present five use cases showcasing the capabilities of OnToxKG. The first three focus on integrating symbol data with finer-grained semantic layers through WordNet synset extraction and named entity recognition. The latter two explore how OnTox facilitates the representation and analysis of memes, assessing their semantics and potential toxicity using OnToxKG. Each use case includes a description of its relevance and a corresponding SPARQL query. We provide a couple of SPARQL queries for guidance; additional queries and full results are accessible on GitHub.

### Symbol-Based Use Cases

#### Query 1. Top Pairs of Symbols Grouped by Shared Concepts

The query lists pairs of potentially toxic symbols sharing the most concepts, revealing semantic connections based on shared conceptual references. Symbol `symbol_565` (Proud Boys of Columbus logo) and `symbol_490` (New Hampshire Proud Boys logo) exhibit the most overlap, sharing 103 concepts. The top 50 pairs also relate to chapters of the Proud Boys, indicating significant thematic overlap within the KG.

```sparql
SELECT ?symbol1 ?symbol2 (COUNT(?sharedConcept) AS ?sharedConceptCount)
WHERE {
  ?symbol1 rdf:type ontox:PotentiallyToxicSymbol .
  ?symbol2 rdf:type ontox:PotentiallyToxicSymbol .
  FILTER (?symbol1 != ?symbol2)
  ?symbol1 ontox:relatedToConcept ?sharedConcept .
  ?symbol2 ontox:relatedToConcept ?sharedConcept .
}
GROUP BY ?symbol1 ?symbol2
ORDER BY DESC(?sharedConceptCount)
```


#### Query 2. Named Entities Associated with a Specific Symbol

The query retrieves named entities associated with a specific symbol's descriptions. For example, `symbol_549` (Pinochet's helicopters) is linked to named entities such as Chilean, Right Wing Death Squad, Proud Boys, Anti-Communist Action, and Augusto Pinochet. These results align closely with our manual investigations, showcasing the effectiveness of automated scripts in precisely extracting relevant named entities.


```sparql
SELECT ?label
WHERE {
  ?symbol rdf:type :PotentiallyToxicSymbol ;
          :hasOnToxId "Symbol_549" ;
          :relatedToConcept ?concept .
  ?concept rdf:type :WikiConcept ;
           rdfs:label ?label .
}
```
#### Query 3. Symbols Explicitly Mentioning a Specific Named Entity

This query retrieves symbols from OnTox that explicitly mention a specific named entity via its Wikidata node. For instance, querying for Pepe the Frog identifies symbols `symbol_182` (Clown World), `symbol_381` (Kekistan Flag), `symbol_441` (Moon Man), `symbol_529` (Parteiadler/Reichsadler (Nazi Eagle)), `symbol_543` (Pepe the Frog), and `symbol_693` (The Groyper). These findings underscore OnTox's ability to identify symbols associated with significant cultural, historical, political, and fictional figures, providing valuable insights into thematic affinities and semantic connections within the dataset.

```sparql
SELECT ?symbol ?symbolLabel
WHERE {
  ?symbol rdf:type ontox:PotentiallyToxicSymbol ;
          ontox:relatedToConcept wiki:Q368 .
  OPTIONAL {
    ?symbol rdfs:label ?symbolLabel .
  }
}
```

### Meme-Based Use Cases

#### Query 4. Top Conceptual Similarity to Potentially Toxic Symbols

This query identifies how many concepts are shared between a specific meme and potentially toxic symbols, providing the labels of these symbols along with the count of shared concepts. By applying the query to different memes, we can determine which symbols are most relevant to each meme and which meme shares more concepts with potentially toxic symbols, indicating a higher association with toxic content. For example, when comparing a 4/20 meme related to Hitler's birthday (Hipster Hitler meme) and another related to weed (see Figure Y), the results show that the Hitler meme shares more concepts with symbols associated with Nazism. Specifically, symbols like HH, National Socialist Black Metal, and Roman Salute exhibit the highest overlap. Both memes share concepts with the symbol 4/20, but the Hitler meme has more shared concepts with 4/20 than the weed meme. This indicates that our ontology and knowledge graph effectively capture thematic affinities and semantic connections between potentially toxic symbols and memes, demonstrating the utility of OnTox in identifying and analyzing these relationships.

```sparql
SELECT ?instance ?symbol_label (COUNT(?concept) AS ?sharedConceptCount)
 WHERE {
    ?instance rdf:type ontox:Meme .
    ?instance rdfs:label "meme_3"^^xsd:string ;
                :relatedToConcept ?concept ;
                :hasEmbeddedText ?text .
    ?symbol rdf:type ontox:PotentiallyToxicSymbol ;
    ontox:relatedToConcept ?concept ;
    rdfs:label ?symbol_label .
    ?concept rdfs:label ?concept_label .
}
ORDER BY DESC(?sharedConceptCount)
```

#### Query 5. Concept Mention and Modality Detection

The query checks whether a concept is mentioned in a meme and identifies the modality in which it is mentioned. For example, when we analyze the I Need Rahowa meme to see if it mentions Racial Holy War (Q15994152), the results show that this concept is mentioned in the textual modality. This finding indicates that our system can detect the presence and modality of specific concepts within memes.

```sparql
SELECT ?instance ?text ?concept_label ?mmcd ?tcd ?vcd WHERE {
    ?instance rdf:type ontox:Meme .
    OPTIONAL {
        ?instance :hasEmbeddedText|:hasMultimodalContentDescription|
        :hasTextContentDescription|:hasVisualContentDescription ?content .
        ?content :mentionsConcept ?concept .
    }
    OPTIONAL { ?instance :hasEmbeddedText ?text . }
    OPTIONAL { ?content rdf:type/rdfs:label ?concept_label . }
    FILTER(?concept = <http://www.wikidata.org/entity/Q15994152>)

```