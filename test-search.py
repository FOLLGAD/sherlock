from langchain.utilities import GoogleSerperAPIWrapper, BashProcess

search = GoogleSerperAPIWrapper()
r = search.run("How to enable streaming for langchain with gpt-3.5-turbo")
print(r)
