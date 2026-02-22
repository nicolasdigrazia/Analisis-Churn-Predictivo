import joblib
import pandas as pd

# Cargamos el modelo y las columnas
model = joblib.load('modelo_churn.pkl')
model_columns = joblib.load('model_columns.pkl')

def predecir():
    print("\n--- ORÁCULO SANTANDER ---")
    # Pedimos lo básico
    data = {
        'meses_activo': [int(input("Meses activo: "))],
        'soporte_tickets': [int(input("Tickets: "))],
        'edad': [int(input("Edad: "))],
        'ingreso_total': [float(input("Ingreso: "))],
        'ciudad': [input("Ciudad (Rosario/Cordoba/Buenos aires): ")],
        'producto': [input("Producto (Tv/Internet/Telefonia): ")],
        'medio_pago': [input("Pago (Efectivo/Tarjeta/Transferencia): ")]
    }
    
    # Creamos el DF y aplicamos los mismos Dummies que en el entrenamiento
    df_input = pd.DataFrame(data)
    df_input = pd.get_dummies(df_input)
    
    # Reindexamos para que tenga las mismas columnas que el X_train (pone 0 en las que faltan)
    df_final = df_input.reindex(columns=model_columns, fill_value=0)
    
    # Predecimos
    prob = model.predict_proba(df_final)[0][1]
    print(f"\nProbabilidad de Churn: {prob:.2%}")

if __name__ == "__main__":
    predecir()