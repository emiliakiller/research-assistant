# Research Assistant

A research assistant that will help generate a research paper and answer the user's questions to the best of its ability.

- Objective: Provide the application with a question or series of questions, and have it return an answer and a suitable explaination thereof, as well as a document containing a summary of those findings along with sources used as a report from its interactions with the user.
- Purpose: To obtain a better understanding of AI agents, including their interaction with web APIs, local databases and retrieval augmented generation (RAG), tool usage, embeddings, and the limitations of all of the above

---

## Notes

- When should the model save data?
  - At the end of a session - User might kill program before saving? or might not want to save the program output?
  - Store output in db? no, rather store api responses (whatever is valuable thereof) to db, but save summary output.
  - Storing info in the db would be good for having the model "grow" with usage. Use db contents for embeddings? What, actually, *are* embeddings?
- Model flow: Get user question (use llm?) -> use model to break it down if applicable -> get search results and wikipedia pages relevant to topic (breadth-first search) if not already in db - save data to db -> construct a summary of that information to use to answer user question -> See if user has follow-up questions (repeat)
- What are the limits of RAG/model comprehension/database access/embeddings?
