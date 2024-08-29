
def check_yes_no(answer):
    if answer.lower() in ['yes', 'y']:
        return True
    elif answer.lower() in ['no', 'n']:
        return False
    else:
        return None

def rule_start():
    question = 'Are you sick?'
    answer = input(question)
    while(check_yes_no(answer) is None):
        print('Non valid input, please type either yes or no')
        answer = input(question)

    if check_yes_no(answer):
        rule_0()
    else:
        rule_food_0()

def rule_food_0():
    question = 'Thats great! Then we will get you something to eat. Do you want soup?'
    answer = input(question)
    while(check_yes_no(answer) is None):
        print('Non valid input, please type either yes or no')
        answer = input(question)

    if check_yes_no(answer):
        rule_food_1()
    else:
        rule_food_6()

def rule_food_1():
    question = 'Do you want fish in your soup?'
    answer = input(question)
    while(check_yes_no(answer) is None):
        print('Non valid input, please type either yes or no')
        answer = input(question)

    if check_yes_no(answer):
        print('You will eat fishsoup')
        exit()
    else:
        rule_food_2()

def rule_food_2():
    question = 'Do you want meat in your soup?'
    answer = input(question)
    while(check_yes_no(answer) is None):
        print('Non valid input, please type either yes or no')
        answer = input(question)

    if check_yes_no(answer):
        rule_food_3()
    else:
        print('Today is your lucky day! You will eat cauliflower soup')
        exit()

def rule_food_3():
    question = '''Do you want two or more of the following ingrediants? 
                    -Broccoli
                    -Carrots
                    -Corn
                '''
    answer = input(question)
    while(check_yes_no(answer) is None):
        print('Non valid input, please type either yes or no')
        answer = input(question)

    if check_yes_no(answer):
        rule_food_4()
    else:
        rule_food_5()

def rule_food_4():
    question = 'Do you want red meat in your soup?'
    answer = input(question)
    while(check_yes_no(answer) is None):
        print('Non valid input, please type either yes or no')
        answer = input(question)

    if check_yes_no(answer):
        print('MOOOO! this will be a good meatsoup')
        exit()
    else:
        print('I love chickensoup, and you will love it too!')
        exit()

def rule_food_5():
    question = 'Do you want red chicken in your soup?'
    answer = input(question)
    while(check_yes_no(answer) is None):
        print('Non valid input, please type either yes or no')
        answer = input(question)

    if check_yes_no(answer):
        print('I love chickensoup, and you will love it too!')
        exit()
    else:
        print('If you dont want any meat in your soup, you will eat tofu!')
        exit()

def rule_food_6():
    question = 'Do you want to eat fish?'
    answer = input(question)
    while(check_yes_no(answer) is None):
        print('Non valid input, please type either yes or no')
        answer = input(question)

    if check_yes_no(answer):
        rule_food_7()
    else:
        rule_food_8()

def rule_food_7():
    question = '''Do you want two or more of the following ingrediants? 
                    -Rice
                    -Soy sauce
                    -Onion
                '''
    answer = input(question)
    while(check_yes_no(answer) is None):
        print('Non valid input, please type either yes or no')
        answer = input(question)

    if check_yes_no(answer):
        print('Fish is good for you! Especially when you combine it with rice')
        exit()
    else:
        print('This will be delicious, you will make a pizza!')
        exit()

def rule_food_8():
    question = 'Do you want to eat chicken?'
    answer = input(question)
    while(check_yes_no(answer) is None):
        print('Non valid input, please type either yes or no')
        answer = input(question)

    if check_yes_no(answer):
        print('This will be delicious, you will make a pizza!')
        exit()
    else:
        rule_food_9()

def rule_food_9():
    question = 'Do you want beard with your meal?'
    answer = input(question)
    while(check_yes_no(answer) is None):
        print('Non valid input, please type either yes or no')
        answer = input(question)

    if check_yes_no(answer):
        rule_food_10()
    else:
        print('You will make the best norwegian dish, meatcakes in brownsauce!')
        exit()

def rule_food_10():
    question = 'Are you sure?'
    answer = input(question)
    while(check_yes_no(answer) is None):
        print('Non valid input, please type either yes or no')
        answer = input(question)

    if check_yes_no(answer):
        rule_0()
    else:
        print('Huff, dodged a bullet there! You will eat chili con carne')
        exit()

def rule_0():
    question = 'Do you have small or large red dots on your skin?'
    answer = input(question)
    while(check_yes_no(answer) is None):
        print('Non valid input, please type either yes or no')
        answer = input(question)

    if check_yes_no(answer):
        rule_1()
    else:
        rule_3()


def rule_1():
    question = '''Do you have two or more of the following symptoms? 
                    -Snuffy
                    -Bloodshot eyes
                    -Dry cough
                '''
    answer = input(question)
    while(check_yes_no(answer) is None):
        print('Non valid input, please type either yes or no')
        answer = input(question)

    if check_yes_no(answer):
        print("You might have measles")
        exit()
    else:
        rule_2()

def rule_2():
    question = 'Are you swollen in the back of your neck or on the side of your throat?'
    answer = input(question)
    while(check_yes_no(answer) is None):
        print('Non valid input, please type either yes or no')
        answer = input(question)

    if check_yes_no(answer):
        print("You might have rubella")
    else:
        rule_3()

def rule_3():
    question = 'Do you have red, ithcy dots'
    answer = input(question)
    while(check_yes_no(answer) is None):
        print('Non valid input, please type either yes or no')
        answer = input(question)

    if check_yes_no(answer):
        print("You might have chicken pox")
        exit()
    else:
        rule_4()

def rule_4():
    question = 'Do you have a minor area with red dots?'
    answer = input(question)
    while(check_yes_no(answer) is None):
        print('Non valid input, please type either yes or no')
        answer = input(question)

    if check_yes_no(answer):
        rule_5()
    else:
        print("I don't know what is wrong, you might want to contact a doctor")

def rule_5():
    question = '''Do you have two or more of the following symptoms? 
                    -Cramps
                    -Headache
                    -Light sensitivity
                    -Pain when tilting your head forwards
                '''
    answer = input(question)
    while(check_yes_no(answer) is None):
        print('Non valid input, please type either yes or no')
        answer = input(question)

    if check_yes_no(answer):
        print("You should contact a doctor! This might be signs of allergic purpura.")
        exit()
    else:
        print("Contact a doctor at once! This might be signs of braindamage")
        exit()

def rule_6():
    question = '''Do you have two or more of the following symptoms? 
                    -Cramps
                    -Headache
                    -Light sensitivity
                    -Pain when tilting your head forwards
                '''
    answer = input(question)
    while(check_yes_no(answer) is None):
        print('Non valid input, please type either yes or no')
        answer = input(question)

    if check_yes_no(answer):
        print("You should contact a doctor! This might be signs of allergic purpura.")
        exit()
    else:
        print("Contact a doctor at once! This might be signs of braindamage")
        exit()

if __name__ == '__main__':
    rule_start()