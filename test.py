import re 

contents = 'hello ,iam_a90 back!!!_hehe '
content = re.sub('\W+', '?', contents)

print(content)