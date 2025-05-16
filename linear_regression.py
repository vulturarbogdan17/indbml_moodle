import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, precision_score, recall_score, f1_score, classification_report

# 1. Încărcarea datelor
data = pd.read_csv('student_activity.csv')

# 2. Selectarea atributelor relevante
features = ['assign_clicks', 'quiz_clicks', 'forum_clicks', 
            'resource_clicks', 'url_clicks']
X = data[features]
y = data['final_grade_binary']  # Variabilă binară (0 sau 1)

# 3. Normalizarea datelor
scaler = MinMaxScaler()
X_normalized = scaler.fit_transform(X)

# 4. Împărțirea datelor
X_train, X_test, y_train, y_test = train_test_split(
    X_normalized, y, test_size=0.3, random_state=42)

# 5. Antrenarea modelului de regresie liniară
model = LinearRegression()
model.fit(X_train, y_train)

# 6. Evaluarea modelului
y_pred = model.predict(X_test)

# Transformăm predicțiile continue în clase binare (0 sau 1)
y_pred_class = np.where(y_pred > 0.5, 1, 0)

# Metrici de regresie
print("Metrici de regresie:")
print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
print("R-squared:", r2_score(y_test, y_pred))

# Metrici de clasificare
print("\nMetrici de clasificare:")
print("Acuratețe:", accuracy_score(y_test, y_pred_class))
print("Precizie:", precision_score(y_test, y_pred_class))
print("Recall:", recall_score(y_test, y_pred_class))
print("F1-score:", f1_score(y_test, y_pred_class))
print("\nRaport de clasificare:\n", classification_report(y_test, y_pred_class))

# Coeficienții modelului
print("\nCoeficienții modelului:")
for feature, coef in zip(features, model.coef_):
    print(f"{feature}: {coef:.4f}")
print(f"\nIntercept (termen liber): {model.intercept_:.4f}")

# Importanța caracteristicilor (valori absolute ale coeficienților)
feature_importance = pd.DataFrame({
    'Feature': features,
    'Coefficient': model.coef_,
    'Absolute_Importance': abs(model.coef_)
}).sort_values('Absolute_Importance', ascending=False)

print("\nImportanța caracteristicilor (valori absolute ale coeficienților):\n", feature_importance)