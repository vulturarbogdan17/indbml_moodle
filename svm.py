import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                            f1_score, classification_report, confusion_matrix,
                            roc_auc_score, RocCurveDisplay)

# 1. Încărcarea datelor
data = pd.read_csv('student_activity.csv')

# 2. Selectarea atributelor relevante
features = ['assign_clicks', 'quiz_clicks', 'forum_clicks', 
            'resource_clicks', 'url_clicks']
X = data[features]
y = data['final_grade_binary']  # Variabilă binară (0 sau 1)

# 3. Normalizarea datelor (important pentru SVM)
scaler = MinMaxScaler()
X_normalized = scaler.fit_transform(X)

# 4. Împărțirea datelor
X_train, X_test, y_train, y_test = train_test_split(
    X_normalized, y, test_size=0.3, random_state=42)

# 5. Antrenarea modelului SVM
model = SVC(kernel='linear', probability=True, random_state=42)  # Kernel liniar pentru interpretabilitate
model.fit(X_train, y_train)

# 6. Evaluarea modelului
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]  # Probabilități pentru clasa 1

# Metrici de clasificare
print("\nMetrici de clasificare:")
print("Acuratețe:", accuracy_score(y_test, y_pred))
print("Precizie:", precision_score(y_test, y_pred))
print("Recall:", recall_score(y_test, y_pred))
print("F1-score:", f1_score(y_test, y_pred))
print("AUC-ROC:", roc_auc_score(y_test, y_proba))
print("\nMatrice de confuzie:\n", confusion_matrix(y_test, y_pred))
print("\nRaport de clasificare:\n", classification_report(y_test, y_pred))

# Importanța caracteristicilor (doar pentru kernel liniar)
if model.kernel == 'linear':
    feature_importance = pd.DataFrame({
        'Feature': features,
        'Coefficient': model.coef_[0],
        'Absolute_Importance': abs(model.coef_[0])
    }).sort_values('Absolute_Importance', ascending=False)
    
    print("\nImportanța caracteristicilor (coeficienți SVM):\n", feature_importance)

# Vizualizare curba ROC
RocCurveDisplay.from_estimator(model, X_test, y_test)
import matplotlib.pyplot as plt
plt.title('Curba ROC pentru modelul SVM')
plt.show()