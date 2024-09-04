import webbrowser

user_input = input('Give a link: ')

def func(user_input):
    webbrowser.open(user_input)

func(user_input)