# from llm_helper import llm
# from few_shot import FewShotPosts
#
# few_shot = FewShotPosts()
#
# def get_length_str(length):
#     if length == "Short":
#         return "1 to 5 lines"
#     if length == "Medium":
#         return "6 to 10 lines"
#     if length == "Long":
#         return "11 to 15 lines"
#
#
# def get_prompt(length, language, tag):
#     length_str = get_length_str(length)
#     prompt = f'''
#         Generate a LinkedIn post using the below information. No preamble.
#
#         1) Topic: {tag}
#         2) Length: {length_str}
#         3) Language: {language}
#         If Language is Hinglish then it means it is a mix of Hindi and English.
#         The script for the generated post should always be English.
#         '''
#
#     examples = few_shot.get_filtered_posts(length, language, tag)
#
#     if len(examples) > 0:
#         prompt += "4) Use the writing style as per the following examples."
#
#         for i, post in enumerate(examples):
#             post_text = post['text']
#             prompt += f'\n\n Example {i + 1}: \n\n {post_text}'
#
#             if i == 1:  # Use max two samples
#                 break
#
#     return prompt
#
#
# def generate_post(length, language, tag):
#     prompt = get_prompt(length, language, tag)
#     response = llm.invoke(prompt)
#     return response.content
#
#
#
# if __name__ == "__main__":
#     post = generate_post("Medium", "English", "Data Science")
#     print(post)



from llm_helper import llm
from few_shot import FewShotPosts

few_shot = FewShotPosts()

def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11 to 15 lines"

def get_prompt(length, language, tag, influencer):
    length_str = get_length_str(length)
    prompt = f'''
        Generate a LinkedIn post using the below information. No preamble.

        1) Topic: {tag}
        2) Length: {length_str}
        3) Language: {language}
        If Language is Hinglish then it means it is a mix of Hindi and English. 
        The script for the generated post should always be written in the Latin/English alphabet.
        '''

    # Filter few-shot context examples directly matching this specific influencer
    examples = few_shot.get_filtered_posts(length, language, tag, influencer)

    if len(examples) > 0:
        prompt += f"\n4) Use the specific professional writing style and tone of {influencer} as shown in these examples."
        for i, post in enumerate(examples):
            prompt += f'\n\n Example {i + 1}: \n\n {post["text"]}'
            if i == 1:
                break
    else:
        prompt += f"\n4) Mimic the professional profile style of {influencer}."

    return prompt

def generate_post(length, language, tag, influencer):
    prompt = get_prompt(length, language, tag, influencer)
    response = llm.invoke(prompt)
    return response.content