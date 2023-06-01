import pandas as pd
import matplotlib.pyplot as plt

def read_csv_file(path):
    with open(path, 'r') as file:
        csv_reader = csv.DictReader(file)
        data = [row for row in csv_reader]
    return pd.DataFrame(data)

def show_table(data):
    table = ttk.Treeview()
    table['columns'] = tuple(data.columns)
    table['show'] = 'headings'

    for column in data.columns:
        table.heading(column, text=column)
        table.column(column, width=100)

    for row in data.itertuples(index=False):
        table.insert('', 'end', values=tuple(row))

    table.pack(expand=True, fill=tk.BOTH)

    button_save_csv = ttk.Button(text="Save as CSV", command=lambda: save_data_as_csv(data))
    button_save_csv.pack()

    button_save_excel = ttk.Button(text="Save as Excel", command=lambda: save_data_as_excel(data))
    button_save_excel.pack()

def save_data_as_csv(data):
    messagebox.showinfo("Save as CSV", "Data saved as CSV file.")
    data.to_csv('data.csv', index=False)

def save_data_as_excel(data):
    messagebox.showinfo("Save as Excel", "Data saved as Excel file.")
    data.to_excel('data.xlsx', index=False)

def read_text_file(path):
    with open(path, 'r') as file:
        lines = file.readlines()

    data = [line.strip().split('|') for line in lines]
    headers = data[0]
    data = data[1:]

    return pd.DataFrame(data, columns=headers)

def show_plot(data):
    plt.figure(figsize=(8, 6))
    data['d_estado'].value_counts().plot(kind='bar')
    plt.xlabel('Estado')
    plt.ylabel('Cantidad')
    plt.title('Distribución de códigos postales por estado')
    plt.xticks(rotation=45)
    plt.show()

def show_tree_view(data):
    tree_view = ttk.Treeview()
    tree_view['columns'] = ('Ciudad', 'Colonia', 'Calles', 'Código Postal')

    tree_view.column('#0', width=100, minwidth=100)
    tree_view.column('Ciudad', width=100, minwidth=100)
    tree_view.column('Colonia', width=100, minwidth=100)
    tree_view.column('Calles', width=100, minwidth=100)
    tree_view.column('Código Postal', width=100, minwidth=100)

    tree_view.heading('#0', text='Estado', anchor=tk.W)
    tree_view.heading('Ciudad', text='Ciudad', anchor=tk.W)
    tree_view.heading('Colonia', text='Colonia', anchor=tk.W)
    tree_view.heading('Calles', text='Calles', anchor=tk.W)
    tree_view.heading('Código Postal', text='Código Postal', anchor=tk.W)

    states = set(data['d_estado'])

    for state in states:
        state_node = tree_view.insert('', 'end', text=state)
        cities = set(data[data['d_estado'] == state]['D_mnpio'])

        for city in cities:
            city_node = tree_view.insert(state_node, 'end', text=city)
            zip_codes = data[(data['d_estado'] == state) & (data['D_mnpio'] == city)]['d_codigo']

            for zip_code in zip_codes:
                zip_code_node = tree_view.insert(city_node, 'end', text=zip_code)
                streets = data[(data['d_estado'] == state) & (data['D_mnpio'] == city) & (data['d_codigo'] == zip_code)]['d_asenta']

                for street in streets:
                    tree_view.insert(zip_code_node, 'end', values=('', '', street, ''))

    tree_view.pack(expand=True, fill=tk.BOTH)
