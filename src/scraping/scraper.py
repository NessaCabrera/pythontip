import requests #Importar el request para hacer las solicitudes http
from bs4 import BeautifulSoup #Importamos BeautifulSoup para nalizar los documentos HTML
import pandas as pd #Immportamos padas para manejar datos en los DataFrames

def fetch_page(url):
    """Obtenemos el contenido de una pagina."""
    response=requests.get(url)#Realizamos una solicitud Get a la URL proporcionada
    if response.status_code == 200: #Comparamos el estatus code con el 200 que significa que fue una peticion exitosa
        return response.content #Devolvemos el contenido de la pagina si la solicitud fue exitosa
    else:
        raise Exception(f"Failed to fetch page: {url}")#lanzamos una excepcion por si la solicitud falla
    
def parse_product(product):
    """Analizamos los detalles de un producto"""
    title= product.find("a", class_="title").text.strip()#Encontramos y obtenemos el titulo del producto
    description=product.find("p", class_="description").text.strip()#Encontramos y obtenemos la descripcion del producto
    price=product.find("h4", class_="price").text.strip()#Encontramos y obtenemos el precio del producto
    return   {
        "title":title,#Retornamos un diccionario con el titulo, descripcion y precio del producto 
        "description":description,
        "price":price,
    }

def scrape(url):
    """Funcion pruncipal del scraping"""
    page_content=fetch_page(url)#obtenemos el codigo base de la pagina
    soup = BeautifulSoup(page_content, "html.parser") #Analizamos el contenido de la pagina con Beautiful Soup
    print(soup)
    products = soup.find_all("div", class_="thumbnail") #Encontramos todos los elementos div con la clase "thubnail" que representas productos
    print(products)

    products_data=[]

    for product in products:
        product_info=parse_product(product)#Analizamos cada product encontrado
        products_data.append(product_info)#Agregamos los datos del producto a la lista
    
    print(products_data)
    return pd.DataFrame(products_data)

#Definimos el URL base para el scraping
base_url="https://webscraper.io/test-sites/e-commerce/allinone"
#Llamamos a la funcion scrape para obtener los datos de los productos
df = scrape(base_url)
#Imprimimos el DF resultante
print(df)

#Guardamos los datos en un archivo CSV sin incluir el indice

df.to_csv("data/raw/products.csv", index=False)#Guardamos los datos en un archivo CSV sin incluir el indice
