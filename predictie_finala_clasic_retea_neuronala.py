import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

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

# 5. Crearea și antrenarea modelului (perceptron cu un singur neuron)
model = Sequential()
model.add(Dense(1, input_dim=len(features), activation='sigmoid'))  # Un singur neuron

model.compile(optimizer=Adam(learning_rate=0.01),
              loss='binary_crossentropy',
              metrics=['accuracy'])

history = model.fit(X_train, y_train, 
                   epochs=50, 
                   batch_size=32, 
                   validation_split=0.2,
                   verbose=1)

# 6. Evaluarea modelului
y_pred_prob = model.predict(X_test)
y_pred = (y_pred_prob > 0.5).astype(int)  # Convertim probabilitățile în predicții binare

print("Acuratețe:", accuracy_score(y_test, y_pred))
print("\nRaport de clasificare:\n", classification_report(y_test, y_pred))
print("\nMatrice de confuzie:\n", confusion_matrix(y_test, y_pred))

# Importanța caracteristicilor (coeficienții neuronului)
weights = model.layers[0].get_weights()[0]
feature_importance = pd.DataFrame({
    'Feature': features,
    'Importance': abs(weights.reshape(-1))  # Luăm valorile absolute ale ponderilor
}).sort_values('Importance', ascending=False)

print("\nImportanța caracteristicilor (coeficienții neuronului):\n", feature_importance)