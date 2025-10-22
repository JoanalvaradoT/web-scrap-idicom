import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.homedepot.com.mx/s/calentadores?marca=rheem' 

try:
    driver = webdriver.Chrome()
    driver.get(url)
    
    print("Esperando 5 segundos para que la página cargue...")
    time.sleep(5)  

    html_content = driver.page_source
    
    driver.quit()

    soup = BeautifulSoup(html_content, 'html.parser')

    productos_encontrados = []

    contenedores_productos = soup.find_all('div', class_='product-card-padding')

    if contenedores_productos:
        for producto in contenedores_productos:
            nombre_elemento = producto.find('span', class_='product-name')
            precio_elemento = producto.find('p', class_='product-price')
            codigo = producto.find('span', class_='product-sku')

            if nombre_elemento and precio_elemento and codigo:
                nombre = nombre_elemento.text.strip()
                precio = precio_elemento.text.strip()
                codigo = codigo.text.strip()

                productos_encontrados.append({'nombre': nombre, 'precio': precio, 'codigo': codigo})
        
        df = pd.DataFrame(productos_encontrados)

        df.to_excel('productos_homedepot.xlsx', index=True)
        print("Datos extraídos y exportados con éxito a 'productos_homedepot.xlsx'")

    else:
        print("No se encontraron productos con la clase 'product-card-padding'.")
        
except Exception as e:
    print(f"Ocurrió un error: {e}")
