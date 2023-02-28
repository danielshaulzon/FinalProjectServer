message: str = "geen button pressed!!!"
messageWords = message.split()
print(messageWords)
match messageWords:
    case [led, "button", "pressed"]:
        print(led)
    
