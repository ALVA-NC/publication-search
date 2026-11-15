# Prompts to ChatGPT

### Prompt: Architectural sparring

I have proposed the following architecture for retrieving publication records from OpenAlex API and storing them in a DB. A frontend app should allow searching and filtering of the data based on certain criteria. Critially reflect on the tech stack and archiecture arguing for pros and cons.
 1. A python script for OpenAlex
 2. MongoDB
 3. Elastic search
 4. Python Fast API
 5. Vue.js

### Prompt: Docker compose setup

Make a docker-compose.yml setup file with mongoDB and elasticsearch for a local setup given the current state

### Prompt: Index Mapping

Based on the current setup of MongoDB i want you to create a script that reads the publications, extracts the field needed for searching and creating an elastic search index with correct mapping.

### Prompt: Fronted in Vue composition API

Write the content of the components and views given the following structure - a publication card, a publication filter and a search bar component. There will be two views - a search view and a publication detail view. Use composition API and make sure data fetching is separated in another folder.

### Prompt: WCAG and frontend styling

It should conform to WCAG Level AA. I also dont want scoped styles as its confusing when styles are kept in multiple places - instead keep a general global scss styles file.

### Prompt: Tests for frontend and backend

Write unit tests for the current frontend and backend so that I can verify the functionality when making further changes.

### Notes

These were some of the most important prompts where they where verified by reading thoroughly through the code and manually testing it. 
