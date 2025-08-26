def assign_label(row):
    suspicious_flags = 0
    if row['after_hours'] > 3:
        suspicious_flags += 1
    if row['after_hours_device_use'] > 2:
        suspicious_flags += 1
    if row['suspicious_visit'] > 2:
        suspicious_flags += 1
    if row['frequent_usb_activity'] == 1:
        suspicious_flags += 1
    if row['novelty_flag'] == 1:
        suspicious_flags += 1
    return 1 if suspicious_flags >= 2 else 0  # Mark malicious if multiple risky behaviors

features['label'] = features.apply(assign_label, axis=1)

X = features.drop('label', axis=1)
y = features['label']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)

np.random.seed(42)
flip_fraction = 0.2  # 20% flip
num_to_flip = int(len(y_train) * flip_fraction)
flip_indices = np.random.choice(y_train.index, size=num_to_flip, replace=False)
y_train.loc[flip_indices] = 1 - y_train.loc[flip_indices]  # Flip labels

model = models.Sequential([
    layers.Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(32, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()])

# Train the model 
history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=15, batch_size=16)
