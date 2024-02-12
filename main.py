import categories
import recipes
import users


def main():
    while True:
        _choice = input(
            "Valitse vaihtoehto (1=lisää käyttäjiä, 2=kategoriat, 3=reseptit, 4=mausteet, 5=lisää mausteet resepteihin, 6=kokkaa, q=lopeta): ")
        if _choice == 'q':
            break
        elif _choice == '1':
            num_of_users = input("Kuinka monta käyttäjää luodaan  / kierros (oletuksena 1000) ")
            if num_of_users == "":
                num_of_users = 1000
            else:
                num_of_users = int(num_of_users)

            users.insert_roles()

            for i in range(10):
                users.insert_users(num_of_users)
        elif _choice == '2':
            categories.insert_categories()
            categories.insert_ethnic_categories()

        elif _choice == '3':
            recipes.insert_states()
            recipes.insert_recipes()

        elif _choice == '4':
            recipes.insert_ingredients()

        elif _choice == '5':
            recipes.mix_ingredients_and_recipes()

        elif _choice == '6':
            recipes.get_cooking()


if __name__ == '__main__':
    main()
