import streamlit as st
import requests
import base64
import io

def main():
    # Título de la aplicación
    st.title("Generador de Ilustraciones para Cuentos Infantiles")
    st.write("Ingresa una descripción de la escena y genera una ilustración en estilo a lápiz, en blanco y negro, con mucho detalle.")

    # Entrada de texto para la descripción de la escena
    scene = st.text_input("Descripción de la escena:")

    # Botón para generar la ilustración
    if st.button("Generar Ilustración"):
        if not scene.strip():
            st.error("Por favor, ingresa una descripción válida de la escena.")
        else:
            with st.spinner("Generando la ilustración..."):
                # Obtener la clave de API de los secretos de Streamlit
                try:
                    api_key = st.secrets["OPENROUTER_API_KEY"]
                except KeyError:
                    st.error("Clave de API no encontrada. Asegúrate de haber configurado los secretos correctamente.")
                    return

                # Configurar los encabezados de la solicitud
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }

                # Crear el prompt incluyendo el estilo deseado
                prompt = f"{scene}, a lápiz, en blanco y negro, con mucho detalle"

                # Datos de la solicitud
                data = {
                    "model": "meta-llama/llama-3.2-90b-vision-instruct:free",
                    "prompt": prompt,
                    "width": 512,
                    "height": 512,
                    "steps": 50,  # Aumentado para mayor detalle
                    "n": 1,
                    "response_format": "b64_json"
                }

                try:
                    # Realizar la solicitud POST a la API de OpenRouter
                    response = requests.post(
                        "https://openrouter.ai/api/v1/images/generations",
                        headers=headers,
                        json=data
                    )
                    response.raise_for_status()  # Verificar si la solicitud fue exitosa

                    # Procesar la respuesta JSON
                    result = response.json()

                    if "data" in result and len(result["data"]) > 0:
                        image_b64 = result["data"][0].get("b64_json")
                        if image_b64:
                            # Decodificar la imagen de base64
                            image_bytes = base64.b64decode(image_b64)
                            image = io.BytesIO(image_bytes)

                            # Mostrar la imagen en la aplicación
                            st.image(image, caption="Ilustración generada", use_column_width=False)
                        else:
                            st.error("No se encontró la imagen en la respuesta de la API.")
                    else:
                        st.error("Respuesta inesperada de la API.")
                
                except requests.exceptions.HTTPError as http_err:
                    st.error(f"Error HTTP: {http_err}")
                except requests.exceptions.ConnectionError:
                    st.error("Error de conexión. Verifica tu conexión a internet.")
                except requests.exceptions.Timeout:
                    st.error("La solicitud a la API ha excedido el tiempo de espera.")
                except requests.exceptions.RequestException as err:
                    st.error(f"Ocurrió un error: {err}")
                except Exception as e:
                    st.error(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    main()
