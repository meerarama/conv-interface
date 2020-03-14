import sys
import json
import re
import recipe_api


def input_recipe():
    url = ""
    while not url:
        url = input("Recipe URL: ").lower()
        if url == "quit":
            print("Thanks for using ReciParser! Bye!\n")
            sys.exit(0)
        if "allrecipes" not in url:
            print("Invalid URL provided! Please submit again.\n")
            url = ""
    name = recipe_api.get_name(url)
    print(
        "Thanks for submitting that URL! The recipe you requested was " + name + ".\n"
    )
    return url, name


def confirm_recipe(url):
    response = ""
    while not response:
        response = input("Is that the correct recipe? ([y]es/[n]o): ").lower()
        if response == "quit":
            print("Thanks for using ReciParser! Bye!\n")
            sys.exit(0)
        elif response == "no" or response == "n":
            print("No worries! Please provide the correct URL.")
            url = input_recipe()
            response = ""
        elif response == "yes" or response == "y":
            print("Great! Let's get started.")
        else:
            print("Sorry I didn't understand that.")
            response = ""
    return url


def fetch_recipe_info(url, name):

    print(
        "First, we'll fetch the recipe information for you. Sit tight, this might take a minute or two. This will be provided below, as well as in a document for your reference later on."
    )
    fields = ["recipe_name", "ingredients", "tools", "methods", "steps"]
    recipe_data = {c: None for c in fields}

    for f in fields:
        if f == "recipe_name":
            recipe_data[f] = name
        else:
            recipe_data[f] = getattr(recipe_api, "get_%s" % f)(url)

    doc_name = re.sub(r"\W+", "", name.lower())
    with open(doc_name + ".json", "w") as recipe_file:
        json.dump(recipe_data, recipe_file)

    return recipe_data



def main():
    # Begin process
    print(
        "Welcome to ReciParser! Let's get started! \nPlease provide a valid AllRecipes.com URL or type 'quit' to quit the program. You can quit whenever we request your input.\n"
    )
    # Request recipe
    url, name = input_recipe()
    # Confirm URL submitted
    url = confirm_recipe(url)
    # Get data from allrecipes.com
    recipe_info = fetch_recipe_info(url, name)

    steps = recipe_info["steps"]
    print("\n")
    print("You can ask me to show you steps, ingredients, or tools! When specifying step numbers, make sure you use the actual numbers -- like 1, 2, and 3. When you're finished, just let me know you're done!")
    print("\n")
    # Apply transformations (allows for multiple until user wants to stop)
    nq = True
    step_num = 0
    while nq:
        cont = ""
        while not cont:
            cont = input(
                "What would you like to do?"
            ).lower()
            try:
                nums = re.findall("\d+", cont)[0]
                nums = int(nums) - 1
            except:
                nums = [ ]
            if "ingredients" in cont:
                print("\n")
                print("Sure! The list of ingredients is:")
                print("\n")
                for e in recipe_info["ingredients"]:
                    print("- " + e)
                print("\n")
                continue
            if "tools" in cont:
                print("\n")
                print("Sure! The tools list is:")
                print("\n")
                for e in recipe_info["tools"]:
                    print("- " + e)
                print("\n")
                continue
            if "next" in cont:
                if step_num >= len(steps):
                    print("That's all the steps there are!")
                    break
                else:
                    print("\n")
                    print("Sure! The next step is:")
                    print("\n")
                    print("-" + steps[step_num])
                    step_num +=1
                    continue
            if "back" in cont:
                step_num -= 2
                if step_num < 0:
                    print("That's all the steps there are!")
                    break
                else:
                    print("\n")
                    print("Sure! The previous step is:")
                    print("\n")
                    print("-" + steps[step_num - 1])
                    continue
            if "first" in cont:
                step_num = 0
                print("\n")
                print("Sure! The first step is:")
                print("\n")
                print("-" + steps[0])
                step_num +=1
                continue
            if nums != [ ] and "step" in cont:
                if int(nums) >= len(steps):
                    print("Sorry, that step doesn't exist. Try something else?")
                    break
                print("\n")
                print("Sure! That step is:")
                print("\n")
                print("-" + steps[int(nums)])
                continue
            if "done" in cont or "stop" in cont or "quit" in cont:
                nq = False
            else:
                print("Sorry I didn't understand that.")
                cont = ""
    print("Thanks for using ReciParser!\n")
    new_rec_resp = ""
    while not new_rec_resp:
        new_rec_resp = input(
            "Would you like to try another recipe? ([y]es/[n]o):").lower()
        if new_rec_resp == 'y' or new_rec_resp == 'yes':
            main()
        elif new_rec_resp == "n" or cont == "no":
            print("Thanks for using ReciParser!\n")
            sys.exit(0)
        else:
            print("Sorry, I didn't understand that!")
            new_rec_resp = ""

if __name__ == "__main__":
    main()
