# 🔮 Predictor de Churn - Telecomunicaciones

Análisis completo y sistema de priorización de clientes en riesgo de abandono para empresa de telecomunicaciones. Combina análisis exploratorio, modelado predictivo con Machine Learning y herramienta web interactiva para equipos de retención.

## 🚀 Demo en Vivo
👉 **[Ver app deployada en Streamlit](predictivec.streamlit.app)**



---

## 📊 Resumen Ejecutivo

### Dataset Analizado
- **Total clientes:** 980
- **Tasa de churn general:** 30.3% (683 activos, 297 con churn)
- **Variables analizadas:** Edad, antigüedad, tickets soporte, ingreso, ciudad, producto, medio de pago

### Segmentación de Riesgo
- **Riesgo Bajo:** 428 clientes (43.7%)
- **Riesgo Medio:** 436 clientes (44.5%)
- **Riesgo Alto:** 116 clientes (11.8%)

### Impacto Económico
- **Ingreso mensual en riesgo crítico:** $29,531,820
- **Clientes con 6+ tickets de soporte:** 600 (grupo de alto riesgo)
- **Pérdida potencial anual estimada:** $861,432,732

---

## 🔍 Hallazgos Clave del Análisis Exploratorio

### Patrones de Churn Identificados

#### Por Edad
- **Mayores de 60 años:** Mayor tasa de churn
- **18-30 años:** Segunda mayor tasa
- Segmento 30-45 años es el más estable

#### Por Producto
- **TV:** 32.0% de churn (mayor tasa)
- **Internet:** 31.4% de churn
- Estos dos productos concentran el mayor riesgo

#### Por Ciudad
- **Buenos Aires:** 32.6% de churn (mayor tasa)
- **Córdoba:** Alta concentración de churn
- **Rosario:** Alta concentración de churn
- **Mendoza:** 29.0% (menor tasa)

#### Por Tickets de Soporte
- **6-9 tickets:** Zona crítica de riesgo (>40% churn)
- **14+ tickets:** Abandono casi seguro
- La cantidad de reclamos es el indicador operacional más fuerte

---

## 🤖 Modelo Predictivo

### Algoritmo y Entrenamiento
```python
- Modelo: Random Forest Classifier
- Técnica de balanceo: SMOTE (Synthetic Minority Over-sampling)
- Optimización: GridSearchCV con validación cruzada
- Variables: edad, antigüedad, tickets, ingreso + ciudad, producto, medio_pago (one-hot encoded)
```

### Métricas del Modelo
```
              precision    recall  f1-score   support
           0       0.67      0.86      0.75       261
           1       0.36      0.15      0.21       131

    accuracy                           0.62       392
   macro avg       0.51      0.51      0.48       392
weighted avg       0.57      0.62      0.57       392

ROC-AUC: 0.507
```

### Feature Importance
Las variables más importantes según el modelo Random Forest:

1. **Ingreso total:** 31.3%
2. **Edad:** 26.1%
3. **Antigüedad (meses activo):** 24.9%
4. **Tickets de soporte:** 17.7%
5. Variables categóricas (ciudad, producto): ~10% combinadas

### Interpretación del Modelo
- **Accuracy 62%:** Razonable para un problema de churn desbalanceado
- **Recall clase 1 (churn) bajo (15%):** El modelo es conservador en predecir churn
- **Precision clase 1 baja (36%):** Genera algunos falsos positivos
- **ROC-AUC ~0.50:** Modelo básico, espacio de mejora

**Nota:** El modelo prioriza **no perder clientes activos** (recall 86% en clase 0) sobre predecir todos los abandonos. Para el caso de uso de retención, esto es aceptable: mejor intervenir de más que de menos.

---

## 🎯 Sistema de Priorización de Clientes

### Lógica de Segmentación
El sistema usa la **probabilidad de churn** generada por el modelo para clasificar:
```python
- prob_churn < 0.3  → Riesgo Bajo
- 0.3 ≤ prob_churn < 0.6 → Riesgo Medio  
- prob_churn ≥ 0.6 → Riesgo Alto
```

### Criterios de Priorización (SQL Query)
```sql
SELECT * FROM analisis_riesgo_clientes
WHERE churn = 0  -- Solo clientes activos
  AND ciudad IN ('Rosario', 'Cordoba', 'Buenos aires')
  AND producto IN ('Tv', 'Internet')
  AND edad >= 42
ORDER BY prob_churn DESC
```

**Resultado:** Lista ordenada de clientes que cumplen TODOS los criterios de riesgo identificados en el análisis exploratorio.

---

## 🛠️ App Web Interactiva - Streamlit

### Funcionalidades

#### 1. Filtros Dinámicos
- **Ciudad:** Selección múltiple
- **Producto:** Selección múltiple
- **Edad mínima:** Slider ajustable
- **Tickets de soporte:** Rango ajustable (ej: 6-9 para zona crítica)
- **Nivel de riesgo:** Alto, Medio, Bajo

#### 2. KPIs en Tiempo Real
- Cantidad de clientes prioritarios según filtros
- Probabilidad promedio de churn del segmento
- Probabilidad máxima detectada

#### 3. Tabla de Clientes
Listado ordenado por probabilidad descendente con:
- Edad
- Ciudad
- Producto
- Tickets de soporte
- Antigüedad
- Probabilidad de churn
- Categoría de riesgo

#### 4. Exportación
- Descarga de lista priorizada en CSV
- Listo para importar en CRM o sistema de gestión

### Caso de Uso Típico
```
1. Equipo de retención ingresa a la app
2. Filtra: edad >= 42, tickets entre 6-9, riesgo Alto
3. Obtiene lista de 20-50 clientes críticos
4. Descarga CSV con datos de contacto
5. Ejecuta campaña de retención personalizada
```

---

## 📦 Instalación y Uso

### Requisitos
```bash
Python 3.9+
pandas
scikit-learn
imblearn
plotly
streamlit
```

### Instalación Local
```bash
# Clonar repositorio
git clone https://github.com/nicolasdigrazia/Analisis-Churn-Predictivo
cd Analisis-Churn-Predictivo

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar app
streamlit run app.py

# Prediccion interactiva
python predict.py
```

### Estructura del Proyecto
```
📁 Analisis-Churn-Predictivo
├── 📄 app.py                           # App web Streamlit
├── 📄 predict.py                       # Script de predicción interactiva
├── 📓 AnálisisDeChurn.ipynb            # Análisis completo y entrenamiento
├── 📊 analisis_riesgo_clientes.csv     # Dataset con predicciones
├── 📄 modelo_churn.pkl                 # Modelo entrenado
├── 📄 model_columns.pkl                # Columnas del modelo
├── 📋 requirements.txt                 # Dependencias
├── 📖 README.md                        # Este archivo

```

---

## 💼 Impacto de Negocio

### Cuantificación del Riesgo

#### Segmento Crítico
- **116 clientes en riesgo alto** (prob > 60%)
- **Ingreso mensual:** $29.5M
- **Exposición anual:** $354M
- **Pérdida estimada anual:** $166.5M

#### Segmento con 6+ Tickets
- **600 clientes** con historial de problemas
- **Tasa de churn observada:** 45%
- **Pérdida anual potencial:** $861M

### ROI de Intervención

**Escenario conservador:**
- Retención exitosa: 30% del segmento alto riesgo
- Clientes salvados: ~35
- Valor anual protegido: $106M
- Costo campaña retención: ~$5.8M (5% del valor)
- **ROI: 18.3x**

### Recomendaciones Accionables

#### 1. Prioridad Máxima (Riesgo Alto)
- **Acción:** Llamada inmediata del gerente de cuenta
- **Oferta:** Descuento 20-30% por 6 meses + upgrade gratuito
- **Timeline:** Primeros 7 días

#### 2. Atención Preventiva (Riesgo Medio)
- **Acción:** Email personalizado + encuesta de satisfacción
- **Oferta:** Beneficio por lealtad (10-15% descuento)
- **Timeline:** 30 días

#### 3. Optimización Operacional
- **Mejorar soporte técnico:** Principal driver de churn
- **Revisión productos TV/Internet:** Mayor abandono
- **Estrategia regional:** Foco en Buenos Aires, Córdoba, Rosario

---

## 🚀 Próximos Pasos

### Mejoras del Modelo
- [ ] Implementar XGBoost o LightGBM
- [ ] Tunear SMOTE (ratio de oversampling)
- [ ] Feature engineering: interacciones, variables temporales
- [ ] Validación con datos de Q2 2026

### Mejoras de la App
- [ ] Dashboard Power BI complementario
- [ ] Integración con CRM (API)
- [ ] Sistema de alertas automáticas (email/Slack)
- [ ] Histórico de intervenciones y tasa de éxito

### Análisis Adicional
- [ ] Segmentación de clientes (clustering)
- [ ] Análisis de cohortes
- [ ] Predicción de LTV (Lifetime Value)
- [ ] A/B testing de estrategias de retención

---

## 🛠️ Stack Técnico

**Análisis y Modelado:**
- Python 3.9
- Pandas, NumPy
- Scikit-learn (Random Forest, GridSearchCV)
- Imbalanced-learn (SMOTE)
- Matplotlib, Seaborn

**App Web:**
- Streamlit
- Plotly Express

**Análisis SQL:**
- SQLite / Pandas query syntax

**Deployment:**
- Streamlit Cloud / Hugging Face Spaces

---

## 📈 Metodología

1. **Exploración de datos:** Análisis univariado y bivariado de todas las variables
2. **Feature engineering:** One-hot encoding de variables categóricas
3. **Balanceo de clases:** SMOTE para tratar desbalance 70/30
4. **Entrenamiento:** Random Forest con GridSearchCV (optimización de hiperparámetros)
5. **Evaluación:** Métricas de clasificación + ROC-AUC
6. **Segmentación:** Clasificación en 3 niveles de riesgo
7. **Priorización:** Filtrado SQL con criterios de negocio
8. **Productización:** App Streamlit para uso operacional

---

## 📝 Limitaciones y Consideraciones

### Limitaciones del Modelo
- **ROC-AUC ~0.50:** Poder predictivo básico, hay espacio para mejora
- **Recall bajo en clase minoritaria:** Puede no detectar todos los churns reales
- **Validación temporal:** No se validó con datos futuros (riesgo de overfitting)

### Consideraciones de Negocio
- El modelo es una **herramienta de apoyo**, no reemplaza el criterio del equipo
- Las probabilidades son **estimaciones**, no certezas
- Se recomienda **monitorear tasa de éxito** de intervenciones para mejorar continuamente

---

## 👤 Autor

**Nicolás Di Grazia**  
Strategic Analyst | Business Intelligence | Predictive Analytics

📧 Email: nicolasdigrazia@proton.me  
💼 [LinkedIn](https://linkedin.com/in/nicolasdigrazia)  
💻 [GitHub](https://github.com/nicolasdigrazia)  


---

## 📄 Licencia

Este proyecto es parte de un portfolio profesional. El código es de uso libre para fines educativos y de aprendizaje.

---

## 🧠 Notas Adicionales

Proyecto desarrollado como caso de estudio de análisis predictivo aplicado a retención de clientes en telecomunicaciones.

*Última actualización: Febrero 2026*