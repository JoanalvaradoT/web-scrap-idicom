import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import datetime


url = 'https://www.homedepot.com.mx/s/calentadores?marca=rheem'

try:
    options = Options()
    options.add_argument('--headless')  
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    
    print("Esperando 5 segundos para que la página cargue...")
    time.sleep(5)

    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')

    productos_encontrados = []
    contenedores_productos = soup.find_all('div', class_='product-card-padding')

    if contenedores_productos:
        print(f"Se encontraron {len(contenedores_productos)} productos.\n")

        for i, producto in enumerate(contenedores_productos, start=5):
            nombre_elemento = producto.find('span', class_='product-name')
            precio_elemento = producto.find('p', class_='product-price')
            codigo_elemento = producto.find('span', class_='product-sku')
            enlace_elemento = producto.find('a', href=True)

            if nombre_elemento and precio_elemento and codigo_elemento and enlace_elemento:
                nombre = nombre_elemento.text.strip()
                precio = precio_elemento.text.strip()
                codigo = codigo_elemento.text.strip()
                enlace = 'https://www.homedepot.com.mx' + enlace_elemento['href']

                driver.get(enlace)
                time.sleep(5)
                html_detalle = driver.page_source
                soup_detalle = BeautifulSoup(html_detalle, 'html.parser')

                modelo = "No encontrado"
                for e in soup_detalle.find_all(['span', 'p', 'td', 'div']):
                    texto = e.text.strip().lower()
                    if texto.startswith("modelo") or "modelo:" in texto:
                        modelo = e.text.replace("Modelo:", "").strip()
                        break

                productos_encontrados.append({
                    'nombre': nombre,
                    'precio': precio,
                    'codigo': codigo,
                    'modelo': modelo,
                    'url': enlace
                })

                print(f"{nombre} - {precio} - {codigo} - {modelo}")

                driver.back()
                time.sleep(2)

        df = pd.DataFrame(productos_encontrados)
        fecha = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        df.to_excel(f'productos__{fecha}.xlsx', index=False)
        print("\n Datos extraídos y exportados con éxito a 'productos_homedepot.xlsx'")

    else:
        print(" No se encontraron productos con la clase 'product-card-padding'.")

except Exception as e:
    print(f" Ocurrió un error: {e}")

finally:
    driver.quit()
