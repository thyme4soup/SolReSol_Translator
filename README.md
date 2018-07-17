# SolReSol_Translator
A very much WIP SolReSol Translator with synonym lookup

## Overview
The purpose of this project is a language module for an Arduino project. So, in addition to an English to SolReSol translating function, it also offers serialization and (for debugging) play functions. A main issue is that the dictionary (while quite large and amazing, big props to the community that made it and maintain it), is not a true 1:1 translation of English. In an effort to avoid dropping words, I used a thesaurus module to query synonyms. This approach basically eliminates the dropped word issue, but can on occasion slightly (or grossly) change the meaning or part of speech of words.
