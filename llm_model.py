def llm(query):

    output = query + " Blah blah blah END"

    summary = output.split("START")[2]
    summary = summary.split("END")[0]

    return summary