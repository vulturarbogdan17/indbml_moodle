import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# 1. Încărcarea datelor
data = pd.read_csv('student_activity.csv')

# 2. Selectarea atributelor relevante
features = ['assign_clicks', 'quiz_clicks', 'forum_clicks', 
            'resource_clicks', 'url_clicks']
X = data[features]
y = data['final_grade_binary']

# 3. Normalizarea datelor
scaler = MinMaxScaler()
X_normalized = scaler.fit_transform(X)

# 4. Împărțirea datelor
X_train, X_test, y_train, y_test = train_test_split(
    X_normalized, y, test_size=0.3, random_state=42)

# 5. Antrenarea modelului
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 6. Evaluarea modelului
y_pred = model.predict(X_test)

print("Acuratețe:", accuracy_score(y_test, y_pred))
print("\nRaport de clasificare:\n", classification_report(y_test, y_pred))
print("\nMatrice de confuzie:\n", confusion_matrix(y_test, y_pred))

# Importanța caracteristicilor
feature_importance = pd.DataFrame({
    'Feature': features,
    'Importance': model.feature_importances_
}).sort_values('Importance', ascending=False)

print("\nImportanța caracteristicilor:\n", feature_importance)