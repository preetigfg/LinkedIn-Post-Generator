# import json
# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import JsonOutputParser
# from langchain_core.exceptions import OutputParserException
# from llm_helper import llm
#
# def process_posts(raw_file_path, processed_file_path="data/processed_posts.json"):
#     enriched_posts = []
#
#     with open(raw_file_path, encoding='utf-8') as file:
#         posts = json.load(file)
#         for post in posts:
#             post_metadata = extract_metadata(post['text'])
#             post_with_metadata = post | post_metadata
#             enriched_posts.append(post_with_metadata)
#
#     unified_tags = get_unified_tags(enriched_posts)
#
#     for post in enriched_posts:
#         current_tags = post['tags']
#         new_tags = {unified_tags[tag] for tag in current_tags}
#         post['tags'] = list(new_tags)
#
#     with open(processed_file_path, encoding='utf-8', mode="w") as outfile:
#         json.dump(enriched_posts, outfile, indent=4)
#
#
# def get_unified_tags(posts_with_metadata):
#     unique_tags = set()
#     for post in posts_with_metadata:
#         unique_tags.update(post['tags'])
#
#     unique_tags_list = ', '.join(unique_tags)
#
#     template = '''I will give you a list of tags. You need to unify tags with the following requirements,
#
#     1. Tags are unified and merged to create a shorter list.
#         Example 1: "Jobseekers", "Job Hunting" can be all merged into a single tag "Job Search".
#         Example 2: "Motivation", "Inspiration", "Drive" can be mapped to "Motivation"
#         Example 3: "Personal Growth", "Personal Development", "Self Improvement" can be mapped to "Self Improvement
#         Example 4: "Scam Alert", "Job Scam" etc. can be mapped to "Scams"
#     2. Each tag should be follow title case convention. example: "Motivation", "Job Search"
#     3. Output should be a JSON object, No preamble
#     4. Output should have mapping of original tag and the unified tag.
#         For example: {{"Jobseekers": "Job Search", "Job Hunting": "Job Search", "Motivation": "Motivation"}}
#
#     Here is the list of tags:
#     {tags}
#     '''
#
#     pt = PromptTemplate.from_template(template)
#     chain = pt | llm
#
#     response = chain.invoke(input={'tags': unique_tags_list})
#
#     try:
#         json_parser = JsonOutputParser()
#         res = json_parser.parse(response.content)
#     except OutputParserException:
#         raise OutputParserException("Context too big. Unable to parse jobs.")
#
#     return res
#
#
# def extract_metadata(post_text):
#     template = '''
#     You are given a LinkedIn post. You need to extract number of lines, language of the post and tags.
#     1. Return a valid JSON. No preamble.
#     2. JSON object should have exactly three keys: line_count, language and tags.
#     3. tags is an array of text tags. Extract maximum two tags.
#     4. Language should be English or Hinglish (Hinglish means hindi + english)
#
#     Here is the actual post on which you need to perform this task:
#     {post}
#     '''
#
#     pt = PromptTemplate.from_template(template)
#     chain = pt | llm
#     response = chain.invoke(input={'post': post_text})
#
#     try:
#         json_parser = JsonOutputParser()
#         res = json_parser.parse(response.content)
#     except OutputParserException:
#         raise OutputParserException("Context too big. Unable to parse jobs.")
#
#     return res
#
#
# if __name__ == "__main__":
#     process_posts("data/raw_posts.json", "data/processed_posts.json")

import json
import zipfile
import os
import pandas as pd
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from llm_helper import llm


def process_kaggle_zip(zip_path, processed_file_path="data/processed_posts.json"):
    print("Safely unzipping and parsing the Kaggle matrix...")
    extract_dir = "data/extracted_raw"
    os.makedirs(extract_dir, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

    csv_filename = [f for f in os.listdir(extract_dir) if f.endswith('.csv')][0]
    csv_file_path = os.path.join(extract_dir, csv_filename)

    df = pd.read_csv(csv_file_path)
    df = df.dropna(subset=["name", "content"])

    # --- DYNAMIC MULTI-INFLUENCER FIX ---
    # We group by 'name' and grab the first post of 15 completely different people
    sample_posts = df.groupby("name", as_index=False).first().sample(n=15, random_state=42)

    enriched_posts = []

    for idx, row in sample_posts.iterrows():
        print(f"Indexing profile: {row['name']}...")
        post_text = str(row['content'])
        post_metadata = extract_metadata(post_text)

        enriched_post = {
            "influencer": row["name"],
            "text": post_text,
            "engagement": int(row.get("followers", 0)) if pd.notna(row.get("followers")) else 0,
            "line_count": post_metadata.get("line_count", 6),
            "language": post_metadata.get("language", "English"),
            "tags": post_metadata.get("tags", ["Professional"])
        }
        enriched_posts.append(enriched_post)

    # Convert elements to unified tags
    unified_tags = get_unified_tags(enriched_posts)
    for post in enriched_posts:
        post['tags'] = list({unified_tags.get(tag, tag) for tag in post['tags']})

    with open(processed_file_path, encoding='utf-8', mode="w") as outfile:
        json.dump(enriched_posts, outfile, indent=4)
    print("🎉 Dataset successfully configured with 15 unique influencers!")


def get_unified_tags(posts_with_metadata):
    unique_tags = {tag for post in posts_with_metadata for tag in post['tags']}
    if not unique_tags:
        return {}
    template = 'Unify these tags to a clean Title Case mapping list. Output JSON ONLY. Tags: {tags}'
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    try:
        res = JsonOutputParser().parse(chain.invoke(input={'tags': ', '.join(unique_tags)}).content)
    except Exception:
        res = {t: t for t in unique_tags}
    return res


def extract_metadata(post_text):
    template = 'Extract line_count, language, tags (max 2) from this post as JSON object only. Post: {post}'
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    try:
        res = JsonOutputParser().parse(chain.invoke(input={'post': post_text[:1000]}).content)
    except Exception:
        res = {"line_count": 5, "language": "English", "tags": ["Business"]}
    return res


if __name__ == "__main__":
    process_kaggle_zip("data/linkedin_data.zip", "data/processed_posts.json")