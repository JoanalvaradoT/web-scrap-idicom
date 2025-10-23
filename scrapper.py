import time
from selenium import webdriver
from bs4 import BeautifulSoup

url = 'https://www.homedepot.com.mx/b/electrico/centros-de-carga-e-interruptores/centros-de-carga-y-fusibles' 

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

            if nombre_elemento and precio_elemento:
                nombre = nombre_elemento.text.strip()
                precio = precio_elemento.text.strip()

                productos_encontrados.append({'nombre': nombre, 'precio': precio})
        
        for p in productos_encontrados:
            print(f"Producto: {p['nombre']}, Precio: {p['precio']}")
    else:
        print("No se encontraron productos")
        
except Exception as e:
    print(f"Ocurrió un error: {e}")
