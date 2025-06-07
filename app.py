import nltk
from nltk.corpus import movie_reviews, stopwords
from nltk import FreqDist
from nltk import NaiveBayesClassifier
from nltk.classify import accuracy
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import NuSVC
from sklearn.metrics import accuracy_score
import random

print('Массур Вікторія, перша група, лабораторна робота №3\n') #Вивести на екран власне прізвище, ім’я, групу та номер ЛР

# Функція для очистки тексту
def clean_text(text):
    words = [word.lower() for word in movie_reviews.words(text) if word.isalpha()]
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    return words
# Функція для підрахунку кількості входжень слова в список відгуків
def count_word_occurrences(word, reviews):
    return sum(1 for review in reviews for w in movie_reviews.words(review) if w.lower() == word)
# Функція для перевірки наявності слов в файлі
def check_words_in_file(file_path, top_words):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read().lower()

    result_dict = {word: word in text for word in top_words}
    return result_dict


# Завантажуємо корпус movie_reviews
nltk.download('movie_reviews')

# Створюємо список відгуків (за винятком спеціальних символів) та перемішуємо
all_words = [word.lower() for word in movie_reviews.words() if word.isalpha()]
random.shuffle(all_words)

# для підрахунку частоти вживання слів
freq_dist = FreqDist(all_words)

# Виведення 20 найбільш уживаних слів
print("20 найбільш уживаних слів:")
for word, frequency in freq_dist.most_common(20):
    print(f"{word}: {frequency}")

# Пошук кількості вживань слова "happy" серед позитивних та негативних відгуків
word_count_happy_positive = count_word_occurrences('happy', movie_reviews.fileids(categories=['pos']))
word_count_happy_negative = count_word_occurrences('happy', movie_reviews.fileids(categories=['neg']))

print(f"Кількість вживань слова 'happy' серед позитивних відгуків: {word_count_happy_positive}")
print(f"Кількість вживань слова 'happy' серед негативних відгуків: {word_count_happy_negative}")

# значення N
N = 2900

# Створення списку топ N слів
top_words = [word for word, _ in freq_dist.most_common(N)]

# Перевірка наявності слів у файлі cv006_15448.txt (позитивний відгук)
file_path_pos = movie_reviews.abspath('pos/cv006_15448.txt')
result_dict_pos = check_words_in_file(file_path_pos, top_words)

# Виведення словникових значень для перевірених слів у позитивному відгуці
print("Результат перевірки слів у позитивному відгуці:")
print(result_dict_pos)

# Створення списку відгуків та їх класифікація
revs = [(list(movie_reviews.words(fileid)), category) for category in movie_reviews.categories() for fileid in movie_reviews.fileids(category)]
random.shuffle(revs)

# Розділення на тренувальний та тестувальний набори
train_set = revs[:1800]
test_set = revs[1800:]

# Визначення функції для екстракції слів та їх частот
def rev_features(rev):
    rev_words = set(rev)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in rev_words)
    return features

# Визначення найчастіших слів
all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
word_features = list(all_words)

# Створення тренувального та тестувального наборів за допомогою визначених функцій
train_features = [(rev_features(d), c) for (d, c) in train_set]
test_features = [(rev_features(d), c) for (d, c) in test_set]

# Навчання моделі та виведення точності
classifier = NaiveBayesClassifier.train(train_features)
print('Точність класифікації:', accuracy(classifier, test_features))

# Виведення 20 найбільш інформативних ознак
print('20 найінформативніших ознак:')
classifier.show_most_informative_features(20)