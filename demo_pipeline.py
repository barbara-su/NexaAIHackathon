from utils import * 
import argparse
from datetime import datetime 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str, help="user query")
    parser.add_argument("--num_texts", type=int, help="number of contexts to query from database")
    parser.add_argument("--num_instructs", type=int,help="number of instructions generated for each context")
    parser.add_argument("--output_dir", type=str, help="directory to store output", default="demo_result")

    args = parser.parse()
    
    # initialize retriever
    print("initializing retriever...")
    embeddings = CustomJinaEmbeddings()
    vectordb = Chroma(persist_directory="fineweb_db", embedding_function=embeddings)
    retriever = vectordb.as_retriever(search_kwargs={"k": args.num_texts})

    # retrieve num_texts documents and filter
    print("getting contexts...")
    remaining_texts = get_texts_by_query(args.query, args.num_texts, retriever)

    # generate instructions
    print("generating instructions...")
    all_q = gen_m_q_for_n_context(remaining_texts, args.num_instruct, n1=20, n2=20, max_attempt=5)

    # generate answer
    print("searching the web for answer...")
    completed_df = search_for_all_queries(all_q, args.query)

    # save result
    print("saving...")
    current_timestamp = datetime.now()
    completed_df.to_csv(f"{args.query}_{current_timestamp}.csv")

    


    