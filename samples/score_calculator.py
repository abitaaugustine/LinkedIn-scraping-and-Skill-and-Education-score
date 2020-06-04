def calc_score():
    #skill comparison
    f = open("recruiter_skills_require.txt","r")
    text = f.read()
    text = text.split("\n")
    skill_req=[]
    for i in range(len(text)):
        text[i] = text[i].lower()
    for i in text:
	    skill_req.append(i.strip())
    with open('skills.csv', 'r') as t2:
        text= t2.readlines()
        txt=text.pop()
        txt=txt.lower()
        txt = txt.rstrip('\\\n')    #to remove the next line character formed incsv each time a row is added
        skill_list= txt.split(',')
        #print(skill_list)
    skill_score = 0
    for s in skill_list:
        if s in skill_req:
            skill_score = skill_score + 1
    print("skill_score: ", skill_score)
    #print("\nRequirements: ",skill_req)
    #print("\nSkills: ",skill_list)



    #education comparison
    f = open("recruiter_education_require.txt","r")
    text = f.read()
    text = text.split("\n")
    education_req=[]
    education_list=[]
    for i in range(len(text)):
        text[i] = text[i].lower()
    for i in text:
        education_req.append(i.strip())
    with open('education.csv', 'r') as t2:
        text= t2.readlines()
        txt=text.pop()
        temp1=txt.split(',')
        #print(temp1)
        while temp1:
            temp2=temp1.pop()
            temp2=temp2.replace('b\'Degree Name\\n','') #replace the unnecessary details that come in education
            temp2=temp2.replace('\'','')                #as btech is obtained asb'Degree Name\nBTech - Bachelor of Technology'
            temp2=temp2.replace('\\n','')               #on parsing LinkedIn Profile
            temp2=temp2.lower()
            temp2 = temp2.rstrip('\\\n')    #to remove the next line character formed incsv each time a row is added
            #print(temp2)
            education_list.append(temp2)
        #print(education_list)
    education_score = 0
    for s in education_list:
        if s in education_req:
            education_score = education_score + 1
    print("education_score: ", education_score)
    #print("\nRequirements: ",education_req)
    #print("\neducations: ",education_list)