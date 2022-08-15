from tkinter import *
import random
from tkinter import messagebox
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_button_pressed():
    letter_list = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    number_list = list('0123456789')
    symbol_list = list('!@#$%&.!;-:?*%()_-/')

    characters = int(char_entry.get())

    password_numbers = []
    password_symbols = []

    if characters <= 6:
        numbers_amount = random.randint(1, 2)
        for numb in range(numbers_amount):
            password_numbers.append(random.choice(number_list))
        password_symbols.append(random.choice(symbol_list))
    elif 12 >= characters > 6:
        numbers_amount = random.randint(2, 3)
        symbols_amount = random.randint(1, 2)
        for numb in range(numbers_amount):
            password_numbers.append(random.choice(number_list))
        for symbol in range(symbols_amount):
            password_symbols.append(random.choice(symbol_list))
    elif characters > 12:
        numbers_amount = random.randint(2, 5)
        symbols_amount = random.randint(1, 3)
        for numb in range(numbers_amount):
            password_numbers.append(random.choice(number_list))
        for symbol in range(symbols_amount):
            password_symbols.append(random.choice(symbol_list))

    remaining_characters = characters - len(password_numbers) - len(password_symbols)

    password_letters = [random.choice(letter_list) for _ in range(remaining_characters)]
    all_chars_sum = password_letters + password_numbers + password_symbols
    random.shuffle(all_chars_sum)

    password_str = ''
    for value in all_chars_sum:
        password_str += value
    password_entry.delete(0, 'end')
    password_entry.insert(0, password_str)
    password_entry.clipboard_clear()
    password_entry.clipboard_append(password_str)


# ---------------------------- SEARCH FUNCTION ------------------------------- #
def search_button_pressed():
    website = website_entry.get().lower()
    try:
        with open('passwords.json', 'r') as pass_file:
            data_loaded = json.load(pass_file)
    except FileNotFoundError:
        messagebox.showerror(title='Erro', message='Nenhum dado salvo.')
    else:
        if website in data_loaded:
            messagebox.showinfo(title=website.title(),
                                message=f'Usuário/E-mail: {data_loaded[website]["email/usuario"]}\n'
                                        f'Senha: {data_loaded[website]["senha"]}')
            password_entry.clipboard_clear()
            password_entry.clipboard_append(data_loaded[website]["senha"])
        else:
            messagebox.showerror(title='Erro', message='Digite o nome corretamente.')


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_button_pressed():
    data_dict_to_json = {
        website_entry.get(): {
            'email/usuario': user_email_entry.get(),
            'senha': password_entry.get()
        }
    }

    if not password_entry.get() or not user_email_entry.get() or not website_entry.get() or not char_entry.get():
        messagebox.showerror(title='Erro', message='Preencha todos os campos!')
    else:
        save_dialog = messagebox.askokcancel(title=f'Gerenciador de Senhas', message='Gostaria de salvar estes dados?')
        if save_dialog:
            try:
                with open('passwords.json', 'r') as password_data:
                    data_loaded = json.load(password_data)
                    data_loaded.update(data_dict_to_json)
            except FileNotFoundError:
                with open('passwords.json', 'w') as password_data:
                    json.dump(data_dict_to_json, password_data, indent=4)
            else:
                with open('passwords.json', 'w') as password_data:
                    json.dump(data_loaded, password_data, indent=4)
            messagebox.showinfo(title='Gerenciador de Senhas', message='Dados salvos com sucesso.')
            password_entry.delete(0, 'end')
            user_email_entry.delete(0, 'end')
            website_entry.delete(0, 'end')
            website_entry.focus()


# ---------------------------- UI SETUP ------------------------------- #
BLACK = "#212121"
WHITE = '#FFF'
window = Tk()
window.title('Gerenciador de Senhas')
window.config(padx=40, pady=40, background=BLACK)

img = PhotoImage(file='logo/logo.png')

canvas = Canvas(height=300, width=300, background=BLACK, highlightthickness=0)
canvas.create_image(100, 150, image=img)
canvas.grid(row=0, column=1)

website_label = Label(text='Site:', font=('Lucida', 12, 'bold'), background=BLACK, foreground=WHITE)
website_label.grid(row=1, column=0)
user_email_label = Label(text='E-mail/Usuário:', font=('Lucida', 12, 'bold'), background=BLACK, foreground=WHITE)
user_email_label.grid(row=2, column=0)
password_label = Label(text='Senha:', font=('Lucida', 12, 'bold'), background=BLACK, foreground=WHITE)
password_label.grid(row=4, column=0)
character_label = Label(text='Caracteres:', font=('Lucida', 12, 'bold'), background=BLACK, foreground=WHITE)
character_label.grid(row=3, column=0, sticky='w')

website_entry = Entry(width=40)
website_entry.focus()
website_entry.grid(row=1, column=1, pady=5, sticky='w')
user_email_entry = Entry(width=59)
user_email_entry.grid(row=2, column=1, pady=5)
password_entry = Entry(width=30)
password_entry.grid(row=4, column=1, sticky='w', pady=5)
char_entry = Entry(width=5)
char_entry.insert(END, string='12')
char_entry.grid(row=3, column=1, sticky='w')

generate_password_button = Button(text='Gerar Senha', width=20, command=generate_button_pressed)
generate_password_button.grid(row=4, column=1, sticky='e', pady=5)
save_button = Button(text='Salvar', width=50, command=save_button_pressed)
save_button.grid(row=5, column=1, pady=5)
search_button = Button(text='Procurar', width=12, command=search_button_pressed)
search_button.grid(row=1, column=1, sticky='e')

window.mainloop()
