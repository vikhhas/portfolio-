from nltk.corpus import movie_reviews
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import NuSVC
from sklearn.metrics import accuracy_score

# Визначаємо ф-цію для виділення ознак
def extract_features(text):
    return {word: True for word in text.split()}

# Визначаємо тренувальний набір
train_set = [(extract_features(movie_reviews.raw(fileid)), category)
             for category in movie_reviews.categories()
             for fileid in movie_reviews.fileids(category)]

# Конвертуємо тренувальний набір у матрицю
vectorizer = DictVectorizer(sparse=False)
X = vectorizer.fit_transform([features for features, _ in train_set])

# Розбиваємо дані на тренувальний та тестувальний набори
y = [category for _, category in train_set]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1800, random_state=42)

# Тренуємо модель
nu_svc = NuSVC()
nu_svc.fit(X_train, y_train)

y_pred = nu_svc.predict(X_test)

# Оцінити точність
accuracy = accuracy_score(y_test, y_pred)
print(f"Classification accuracy: {accuracy}")