import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                           f1_score, classification_report, confusion_matrix,
                           roc_auc_score, roc_curve)
import matplotlib.pyplot as plt

# 1. Încărcarea datelor
data = pd.read_csv('student_activity.csv')

# 2. Selectarea atributelor relevante
features = ['assign_clicks', 'quiz_clicks', 'forum_clicks', 
            'resource_clicks', 'url_clicks']
X = data[features]
y = data['final_grade_binary']

# 3. Normalizarea datelor (opțional pentru Random Forest)
scaler = MinMaxScaler()
X_normalized = scaler.fit_transform(X)

# 4. Împărțirea datelor
X_train, X_test, y_train, y_test = train_test_split(
    X_normalized, y, test_size=0.3, random_state=42)

# 5. Antrenarea modelului Random Forest
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=5,
    random_state=42,
    class_weight='balanced'  # Important pentru seturi de date dezechilibrate
)
model.fit(X_train, y_train)

# 6. Evaluarea modelului
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

# Metrici de clasificare
print("\nMetrici de clasificare:")
print("Acuratețe:", accuracy_score(y_test, y_pred))
print("Precizie:", precision_score(y_test, y_pred))
print("Recall:", recall_score(y_test, y_pred))
print("F1-score:", f1_score(y_test, y_pred))
print("AUC-ROC:", roc_auc_score(y_test, y_proba))
print("\nMatrice de confuzie:\n", confusion_matrix(y_test, y_pred))
print("\nRaport de clasificare:\n", classification_report(y_test, y_pred))

# Importanța caracteristicilor
feature_importance = pd.DataFrame({
    'Feature': features,
    'Importance': model.feature_importances_
}).sort_values('Importance', ascending=False)

print("\nImportanța caracteristicilor:\n", feature_importance)

# Vizualizare curba ROC
fpr, tpr, _ = roc_curve(y_test, y_proba)
plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (AUC = %0.2f)' % roc_auc_score(y_test, y_proba))
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Curba ROC - Random Forest')
plt.legend(loc="lower right")
plt.show()

# Vizualizare importanță caracteristici
plt.figure(figsize=(10, 6))
plt.barh(feature_importance['Feature'], feature_importance['Importance'])
plt.xlabel('Importanță')
plt.title('Importanța caracteristicilor - Random Forest')
plt.show()