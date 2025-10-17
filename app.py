from flask import Flask
from flask import render_template, request 
import pandas as pd
import folium 

df = pd.read_csv('./static/data_populasi.csv')
app = Flask(__name__)
names = df['nama'].dropna().unique().tolist()

print(names)

@app.route('/', methods=['GET', 'POST'])
def home():
    min_pop = 0
    keyword = ''
    name = ''
    
    if request.method == 'POST':
        min_pop = (request.form.get('min_pop', 0) or 0)
        min_pop = int(min_pop)  
        keyword = request.form.get('keyword', '')
        name = request.form.get('name' , '')
        print(min_pop, keyword, name)

    filtered = df[
        (df['populasi'] >= min_pop) &
        ((df['nama'].str.contains(keyword, case=False, na=False)) &
        (df['nama'].str.contains(name, case=False, na=False)))
        # (df['nama'] == name))
    ]
    # else:
    #     filtered = df
    
    print(df)
    print(filtered)

    m = folium.Map(location=[-6.5, 107.0], zoom_start=5)
    for _, row in filtered.iterrows():    
        popup = f"{row['nama']}<br>Population: {row['populasi']}"
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup= popup,
            tooltip=row['nama']
        ).add_to(m)

    map_html = m._repr_html_()
    return render_template('home.html', map_html=map_html, names=names, selected_name=name, min_pop=min_pop, keyword=keyword)


    # return "Hello, World!"  
#     return '''
#     <h1>Hallo Dunia<h1>


#         <p>Ini adalah halaman utama.</p>
# '''

# @app.route('/about')
# def about():
#     return "this is the about page."

if __name__ == '__main__':
    app.run(debug=True)
