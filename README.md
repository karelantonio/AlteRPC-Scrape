# AlteRPC-Scrape
Vía alternativa para acceder a la Red de Programación Competitiva (Módulo de scraping)

El script `scraping.py` provee una interfaz para acceder al juez BOCA casi como si  fuera el navegador

## ¿Cómo utilizarlo?

Primero debes instalar las dependencias (Requests, BeautifulSoup, PySocks (Opcional, si usas proxy socks5) ):

```sh
pip install requests PySocks bs4
```

El caso de uso más simple es este:

```python
from scraping import AlteRPCClient

#Url del contest-juez virtual
base_url = "https://some.site/contest/2048/13"
api = AlteRPCClient(base=base_url)

#Nos logeamos
if not api.login("user", "pass"):
    #Prueba: "board", "" para ver la tabla
    print("Error accediendo")
    exit(1)

#Obtenemos la tabla
users = api.score()
print("Tabla de usuarios:")
print("#  Ctry  Name")
for user in users:
    print("%-3d %-2s %s" %(
        user.num, user.country, user.name
    ))

#Listo
api.logout()
```

## Contribuir

El proyecto está abierto a contribuciones, pero se deben seguir una serie de pasos para que sea aceptada la solicitud de cambios:

1. Crear un Issue donde describas lo que vas a estar trabajando (y evitar que dos personas esten trabajando en lo mismo)
2. Crearte una copia del repositorio en tu cuenta y clonarlo
3. Crear una nueva rama, con un nombre descriptivo que refleje lo que vas a estar trabajando
4. Realizar los cambios/contribuciones que tienes pensado en esa rama
5. Crear una Pull-Request

## TODOs:

* Descargar el archivo de descripción de los problemas
* Mandar soluciones
* Descargar códigos enviados
* Documentar un poco más el código (especialmente ejemplo)
* Agregar más ejemplos de uso

## Licencia

El código en este repositorio está bajo licencia GNU GPL v2, para mas información debes leer el archivo `LICENSE`