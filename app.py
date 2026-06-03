import json
import sqlite3
from datetime import datetime
from pathlib import Path
from flask import Flask, g, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / 'quiz.db'
SAMPLE_QUIZZES = [
    {
        'id': 'science',
        'title': 'Science',
        'category': 'Science',
        'questions': [
            {'text': 'Which planet is known as the Red Planet?', 'choices': ['Earth', 'Mars', 'Jupiter', 'Venus'], 'answer_index': 1, 'explanation': 'Mars is named after the Roman god of war.'},
            {'text': 'What is the chemical formula for salt?', 'choices': ['NaCl', 'KCl', 'CaCl', 'MgCl'], 'answer_index': 0, 'explanation': 'NaCl is sodium chloride, commonly known as table salt.'},
            {'text': 'How many bones are in the adult human body?', 'choices': ['186', '206', '226', '246'], 'answer_index': 1, 'explanation': 'Adults have 206 bones; babies are born with about 270.'},
            {'text': 'What is the powerhouse of the cell?', 'choices': ['Nucleus', 'Mitochondria', 'Ribosome', 'Lysosome'], 'answer_index': 1, 'explanation': 'Mitochondria generate ATP, the energy currency of cells.'},
            {'text': 'Which gas do plants primarily use for photosynthesis?', 'choices': ['Oxygen', 'Nitrogen', 'Carbon Dioxide', 'Hydrogen'], 'answer_index': 2, 'explanation': 'Plants use CO2 from the air to produce glucose and oxygen.'},
            {'text': 'What is the speed of light in vacuum?', 'choices': ['300,000 km/s', '150,000 km/s', '450,000 km/s', '100,000 km/s'], 'answer_index': 0, 'explanation': 'The speed of light is approximately 299,792 km/s.'},
            {'text': 'What is the largest organ in the human body?', 'choices': ['Heart', 'Brain', 'Liver', 'Skin'], 'answer_index': 3, 'explanation': 'The skin is the largest organ by surface area and weight.'},
            {'text': 'Which metal is liquid at room temperature?', 'choices': ['Gold', 'Silver', 'Mercury', 'Copper'], 'answer_index': 2, 'explanation': 'Mercury is the only metal that is liquid at standard room temperature.'},
            {'text': 'What is the process by which water changes to vapor?', 'choices': ['Condensation', 'Evaporation', 'Sublimation', 'Freezing'], 'answer_index': 1, 'explanation': 'Evaporation is the conversion of liquid water to water vapor.'},
            {'text': 'How many chambers does the human heart have?', 'choices': ['2', '3', '4', '6'], 'answer_index': 2, 'explanation': 'The heart has four chambers: two atria and two ventricles.'},
        ],
    },
    {
        'id': 'history',
        'title': 'History',
        'category': 'History',
        'questions': [
            {'text': 'Which ancient civilization built the pyramids at Giza?', 'choices': ['Romans', 'Greeks', 'Egyptians', 'Mayans'], 'answer_index': 2, 'explanation': 'The Great Pyramids were built by ancient Egyptians during the Old Kingdom.'},
            {'text': 'Who was the first president of the United States?', 'choices': ['Thomas Jefferson', 'George Washington', 'John Adams', 'Benjamin Franklin'], 'answer_index': 1, 'explanation': 'George Washington served as the first U.S. president from 1789 to 1797.'},
            {'text': 'What year did the Berlin Wall fall?', 'choices': ['1987', '1989', '1991', '1993'], 'answer_index': 1, 'explanation': 'The Berlin Wall fell on November 9, 1989, marking the beginning of the end of the Cold War.'},
            {'text': 'In which year did the Titanic sink?', 'choices': ['1910', '1912', '1915', '1920'], 'answer_index': 1, 'explanation': 'The RMS Titanic sank on April 15, 1912, after hitting an iceberg.'},
            {'text': 'Who was the first Emperor of Rome?', 'choices': ['Julius Caesar', 'Augustus', 'Nero', 'Tiberius'], 'answer_index': 1, 'explanation': 'Augustus, originally named Octavian, became the first Roman Emperor in 27 BC.'},
            {'text': 'In which country did the Renaissance begin?', 'choices': ['France', 'Spain', 'Italy', 'Germany'], 'answer_index': 2, 'explanation': 'The Renaissance began in Italy during the 14th century.'},
            {'text': 'What was the main cause of World War I?', 'choices': ['Economic collapse', 'Assassination of Archduke Franz Ferdinand', 'Religious conflict', 'Trade disputes'], 'answer_index': 1, 'explanation': 'The assassination of Archduke Franz Ferdinand triggered the alliance system and led to WWI.'},
            {'text': 'Who wrote the Declaration of Independence?', 'choices': ['George Washington', 'Benjamin Franklin', 'Thomas Jefferson', 'John Adams'], 'answer_index': 2, 'explanation': 'Thomas Jefferson is the primary author of the Declaration of Independence, adopted in 1776.'},
            {'text': 'Which empire was ruled by Napoleon?', 'choices': ['Spanish Empire', 'French Empire', 'British Empire', 'Ottoman Empire'], 'answer_index': 1, 'explanation': 'Napoleon Bonaparte ruled the French Empire from 1804 to 1815.'},
            {'text': 'In what year did Christopher Columbus reach the Americas?', 'choices': ['1490', '1492', '1495', '1500'], 'answer_index': 1, 'explanation': 'Columbus reached the Caribbean islands in 1492, marking the beginning of European colonization.'},
        ],
    },
    {
        'id': 'geography',
        'title': 'Geography',
        'category': 'Geography',
        'questions': [
            {'text': 'What is the capital of France?', 'choices': ['Lyon', 'Marseille', 'Paris', 'Nice'], 'answer_index': 2, 'explanation': 'Paris is the capital and largest city of France.'},
            {'text': 'Which is the longest river in the world?', 'choices': ['Amazon', 'Yangtze', 'Nile', 'Mississippi'], 'answer_index': 2, 'explanation': 'The Nile River in Africa is the longest river at approximately 6,650 km.'},
            {'text': 'What is the highest mountain in the world?', 'choices': ['K2', 'Kangchenjunga', 'Mount Everest', 'Lhotse'], 'answer_index': 2, 'explanation': 'Mount Everest is the highest mountain with a height of 8,849 meters.'},
            {'text': 'Which continent is the coldest?', 'choices': ['Arctic', 'North America', 'Antarctica', 'Asia'], 'answer_index': 2, 'explanation': 'Antarctica is the coldest continent with temperatures dropping below -60°C.'},
            {'text': 'What is the capital of Japan?', 'choices': ['Kyoto', 'Osaka', 'Tokyo', 'Yokohama'], 'answer_index': 2, 'explanation': 'Tokyo has been the capital of Japan since 1868.'},
            {'text': 'Which desert is the largest in the world?', 'choices': ['Kalahari', 'Gobi', 'Sahara', 'Arabian'], 'answer_index': 2, 'explanation': 'The Sahara Desert in Africa is the largest hot desert in the world.'},
            {'text': 'What is the smallest country in the world?', 'choices': ['Monaco', 'Liechtenstein', 'Vatican City', 'San Marino'], 'answer_index': 2, 'explanation': 'Vatican City is an independent city-state and the smallest country at 0.44 km².'},
            {'text': 'Which ocean is the largest?', 'choices': ['Atlantic', 'Indian', 'Arctic', 'Pacific'], 'answer_index': 3, 'explanation': 'The Pacific Ocean is the largest ocean, covering about 46% of the world water surface.'},
            {'text': 'What is the capital of Australia?', 'choices': ['Sydney', 'Melbourne', 'Canberra', 'Brisbane'], 'answer_index': 2, 'explanation': 'Canberra is the capital city of Australia, purpose-built as the capital.'},
            {'text': 'How many continents are there?', 'choices': ['5', '6', '7', '8'], 'answer_index': 2, 'explanation': 'There are 7 continents: Africa, Antarctica, Asia, Europe, North America, Oceania, and South America.'},
        ],
    },
    {
        'id': 'literature',
        'title': 'Literature',
        'category': 'Literature',
        'questions': [
            {'text': 'Who wrote "Romeo and Juliet"?', 'choices': ['Christopher Marlowe', 'William Shakespeare', 'Ben Jonson', 'Edmund Spenser'], 'answer_index': 1, 'explanation': 'William Shakespeare wrote this tragic romance early in his career.'},
            {'text': 'What is the first book in the "Harry Potter" series?', 'choices': ['Chamber of Secrets', 'Philosopher\'s Stone', 'Prisoner of Azkaban', 'Goblet of Fire'], 'answer_index': 1, 'explanation': 'Harry Potter and the Philosopher\'s Stone was published in 1997.'},
            {'text': 'Who wrote "1984"?', 'choices': ['George Orwell', 'Aldous Huxley', 'Ray Bradbury', 'Isaac Asimov'], 'answer_index': 0, 'explanation': 'George Orwell wrote this dystopian novel, published in 1949.'},
            {'text': 'What is the longest novel ever written?', 'choices': ['War and Peace', 'Les Misérables', 'In Search of Lost Time', 'The Brothers Karamazov'], 'answer_index': 2, 'explanation': 'Marcel Proust\'s "In Search of Lost Time" is the longest novel at over 3,000 pages.'},
            {'text': 'Who is the author of "The Great Gatsby"?', 'choices': ['Ernest Hemingway', 'F. Scott Fitzgerald', 'William Faulkner', 'John Steinbeck'], 'answer_index': 1, 'explanation': 'F. Scott Fitzgerald published this American classic in 1925.'},
            {'text': 'What is the main character\'s name in "To Kill a Mockingbird"?', 'choices': ['Atticus', 'Tom', 'Scout', 'Boo'], 'answer_index': 2, 'explanation': 'Scout Finch is the protagonist and narrator of Harper Lee\'s novel.'},
            {'text': 'Who wrote "Pride and Prejudice"?', 'choices': ['Charlotte Brontë', 'Jane Austen', 'Emily Brontë', 'Mary Shelley'], 'answer_index': 1, 'explanation': 'Jane Austen published this romantic novel in 1813.'},
            {'text': 'What is the genre of "The Hobbit"?', 'choices': ['Science Fiction', 'Mystery', 'Fantasy', 'Historical Fiction'], 'answer_index': 2, 'explanation': 'J.R.R. Tolkien\'s "The Hobbit" is a classic fantasy novel.'},
            {'text': 'Who wrote "Moby Dick"?', 'choices': ['Nathaniel Hawthorne', 'Herman Melville', 'Walt Whitman', 'Henry David Thoreau'], 'answer_index': 1, 'explanation': 'Herman Melville wrote this epic novel about Captain Ahab\'s obsession.'},
            {'text': 'What is the real name of the author "Mark Twain"?', 'choices': ['Samuel Clemens', 'Tom Sawyer', 'Henry James', 'James Fennimore Cooper'], 'answer_index': 0, 'explanation': 'Mark Twain was the pen name of Samuel Langhorne Clemens.'},
        ],
    },
    {
        'id': 'sports',
        'title': 'Sports',
        'category': 'Sports',
        'questions': [
            {'text': 'How many players are on a basketball team on the court?', 'choices': ['4', '5', '6', '7'], 'answer_index': 1, 'explanation': 'Each basketball team has 5 players on the court at a time.'},
            {'text': 'In which sport is the term "love" used for a score of zero?', 'choices': ['Badminton', 'Tennis', 'Volleyball', 'Squash'], 'answer_index': 1, 'explanation': 'In tennis, "love" means zero points, possibly derived from the French "l\'œuf" (egg).'},
            {'text': 'How many innings are in a baseball game?', 'choices': ['7', '8', '9', '10'], 'answer_index': 2, 'explanation': 'A standard baseball game consists of 9 innings.'},
            {'text': 'What is the maximum number of clubs a golfer can carry?', 'choices': ['12', '13', '14', '15'], 'answer_index': 2, 'explanation': 'The maximum is 14 clubs per bag according to PGA rules.'},
            {'text': 'In American football, how many points is a touchdown worth?', 'choices': ['5', '6', '7', '8'], 'answer_index': 1, 'explanation': 'A touchdown is worth 6 points; a team can then attempt an extra point.'},
            {'text': 'What is the diameter of a basketball hoop in inches?', 'choices': ['16', '18', '20', '22'], 'answer_index': 1, 'explanation': 'An official NBA hoop has a diameter of 18 inches.'},
            {'text': 'How many Grand Slam tennis tournaments are there per year?', 'choices': ['2', '3', '4', '5'], 'answer_index': 2, 'explanation': 'There are 4 Grand Slam tournaments: Australian Open, French Open, Wimbledon, US Open.'},
            {'text': 'What is the official weight of a soccer ball?', 'choices': ['400-450g', '410-450g', '400-460g', '410-460g'], 'answer_index': 2, 'explanation': 'An official soccer ball weighs between 400 and 460 grams.'},
            {'text': 'In which year was the first modern Olympics held?', 'choices': ['1896', '1900', '1904', '1908'], 'answer_index': 0, 'explanation': 'The first modern Olympic Games were held in Athens, Greece in 1896.'},
            {'text': 'How many players are on a cricket team on the field?', 'choices': ['9', '10', '11', '12'], 'answer_index': 2, 'explanation': 'Each cricket team has 11 players on the field.'},
        ],
    },
    {
        'id': 'mathematics',
        'title': 'Mathematics',
        'category': 'Mathematics',
        'questions': [
            {'text': 'What is the value of pi (π) approximately?', 'choices': ['2.14', '3.14', '4.14', '5.14'], 'answer_index': 1, 'explanation': 'Pi (π) is approximately 3.14159...'},
            {'text': 'What is the square root of 144?', 'choices': ['11', '12', '13', '14'], 'answer_index': 1, 'explanation': '12 × 12 = 144, so √144 = 12.'},
            {'text': 'What is 15% of 200?', 'choices': ['20', '25', '30', '35'], 'answer_index': 2, 'explanation': '15% of 200 = 0.15 × 200 = 30.'},
            {'text': 'What is the sum of angles in a triangle?', 'choices': ['90°', '180°', '270°', '360°'], 'answer_index': 1, 'explanation': 'The sum of all angles in any triangle is 180 degrees.'},
            {'text': 'What is the next prime number after 23?', 'choices': ['24', '25', '29', '31'], 'answer_index': 2, 'explanation': '29 is the next prime number after 23.'},
            {'text': 'What is 2⁵?', 'choices': ['16', '25', '32', '64'], 'answer_index': 2, 'explanation': '2⁵ = 2 × 2 × 2 × 2 × 2 = 32.'},
            {'text': 'What is the area of a circle with radius 5?', 'choices': ['25π', '50π', '75π', '100π'], 'answer_index': 0, 'explanation': 'Area = πr² = π × 5² = 25π.'},
            {'text': 'What is the largest common factor of 12 and 18?', 'choices': ['3', '4', '6', '9'], 'answer_index': 2, 'explanation': 'The GCF of 12 and 18 is 6.'},
            {'text': 'What is the square root of 256?', 'choices': ['14', '15', '16', '17'], 'answer_index': 2, 'explanation': '16 × 16 = 256, so √256 = 16.'},
            {'text': 'What is 50% of 80?', 'choices': ['30', '35', '40', '45'], 'answer_index': 2, 'explanation': '50% of 80 = 0.5 × 80 = 40.'},
        ],
    },
    {
        'id': 'technology',
        'title': 'Technology',
        'category': 'Technology',
        'questions': [
            {'text': 'Who is credited with inventing the World Wide Web?', 'choices': ['Bill Gates', 'Steve Jobs', 'Tim Berners-Lee', 'Linus Torvalds'], 'answer_index': 2, 'explanation': 'Tim Berners-Lee invented the World Wide Web in 1989 while working at CERN.'},
            {'text': 'What does "CPU" stand for?', 'choices': ['Central Processing Unit', 'Central Program Utility', 'Computer Personal Unit', 'Central Processor Utility'], 'answer_index': 0, 'explanation': 'CPU stands for Central Processing Unit, the brain of a computer.'},
            {'text': 'In what year was the first iPhone released?', 'choices': ['2005', '2006', '2007', '2008'], 'answer_index': 2, 'explanation': 'Steve Jobs introduced the first iPhone on June 29, 2007.'},
            {'text': 'What does "HTML" stand for?', 'choices': ['Hyper Text Markup Language', 'High Tech Modern Language', 'Home Tool Markup Language', 'Hyperlinks and Text Markup Language'], 'answer_index': 0, 'explanation': 'HTML is the standard markup language for creating web pages.'},
            {'text': 'Who founded Microsoft?', 'choices': ['Steve Jobs', 'Bill Gates', 'Mark Zuckerberg', 'Larry Page'], 'answer_index': 1, 'explanation': 'Bill Gates and Paul Allen founded Microsoft in 1975.'},
            {'text': 'What does "AI" stand for?', 'choices': ['Automated Intelligence', 'Artificial Intelligence', 'Advanced Internet', 'Automated Internet'], 'answer_index': 1, 'explanation': 'AI stands for Artificial Intelligence, the simulation of human intelligence by machines.'},
            {'text': 'In what year was the first computer bug found?', 'choices': ['1945', '1950', '1955', '1960'], 'answer_index': 0, 'explanation': 'The first computer bug was found in 1945 when a moth was found in a Harvard Mark II computer.'},
            {'text': 'What does "GPU" stand for?', 'choices': ['Graphics Processing Unit', 'General Purpose Utility', 'Graphics Program Unit', 'General Processor Utility'], 'answer_index': 0, 'explanation': 'GPU stands for Graphics Processing Unit, specialized for rendering graphics.'},
            {'text': 'Who founded Google?', 'choices': ['Elon Musk', 'Larry Page and Sergey Brin', 'Mark Zuckerberg', 'Jack Dorsey'], 'answer_index': 1, 'explanation': 'Larry Page and Sergey Brin founded Google in 1998.'},
            {'text': 'What does "VR" stand for?', 'choices': ['Virtual Reality', 'Visual Rendering', 'Vertical Response', 'Video Recording'], 'answer_index': 0, 'explanation': 'VR stands for Virtual Reality, a computer-generated simulation.'},
        ],
    },
]

app = Flask(__name__)


def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
        db = sqlite3.connect(DATABASE_PATH)
        db.row_factory = sqlite3.Row
        g.db = db
    return db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DATABASE_PATH)
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quizzes (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            category TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quiz_id TEXT NOT NULL,
            text TEXT NOT NULL,
            answer_index INTEGER NOT NULL,
            explanation TEXT NOT NULL,
            FOREIGN KEY (quiz_id) REFERENCES quizzes(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS choices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            FOREIGN KEY (question_id) REFERENCES questions(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quiz_id TEXT NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            answers TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (quiz_id) REFERENCES quizzes(id)
        )
    ''')
    db.commit()

    cursor.execute('SELECT COUNT(*) AS count FROM quizzes')
    existing = cursor.fetchone()[0]
    if existing == 0:
        for quiz in SAMPLE_QUIZZES:
            cursor.execute('INSERT INTO quizzes (id, title, category) VALUES (?, ?, ?)',
                           (quiz['id'], quiz['title'], quiz['category']))
            for question in quiz['questions']:
                cursor.execute(
                    'INSERT INTO questions (quiz_id, text, answer_index, explanation) VALUES (?, ?, ?, ?)',
                    (quiz['id'], question['text'], question['answer_index'], question['explanation']),
                )
                question_id = cursor.lastrowid
                for choice in question['choices']:
                    cursor.execute(
                        'INSERT INTO choices (question_id, text) VALUES (?, ?)',
                        (question_id, choice),
                    )
        db.commit()

    db.close()


def query_db(query, args=(), single=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if single else rv


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/quizzes')
def api_quizzes():
    rows = query_db(
        'SELECT q.id, q.title, q.category, COUNT(questions.id) AS question_count '
        'FROM quizzes q LEFT JOIN questions ON q.id = questions.quiz_id GROUP BY q.id'
    )
    data = [
        {
            'id': row['id'],
            'title': row['title'],
            'category': row['category'],
            'question_count': row['question_count'],
        }
        for row in rows
    ]
    return jsonify(data)


@app.route('/api/quiz/<quiz_id>')
def api_quiz(quiz_id):
    quiz = query_db('SELECT id, title, category FROM quizzes WHERE id = ?', (quiz_id,), single=True)
    if quiz is None:
        return jsonify({'error': 'Quiz not found'}), 404

    questions = query_db('SELECT id, text FROM questions WHERE quiz_id = ? ORDER BY id', (quiz_id,))
    quiz_questions = []
    for question in questions:
        choice_rows = query_db('SELECT text FROM choices WHERE question_id = ? ORDER BY id', (question['id'],))
        quiz_questions.append({
            'id': question['id'],
            'text': question['text'],
            'choices': [choice['text'] for choice in choice_rows],
        })

    return jsonify({
        'id': quiz['id'],
        'title': quiz['title'],
        'category': quiz['category'],
        'questions': quiz_questions,
    })


@app.route('/api/result', methods=['POST'])
def api_result():
    payload = request.get_json() or {}
    quiz_id = payload.get('quiz_id')
    answers = payload.get('answers', [])

    if not quiz_id or not isinstance(answers, list):
        return jsonify({'error': 'Invalid submission'}), 400

    questions = query_db('SELECT id, text, answer_index, explanation FROM questions WHERE quiz_id = ? ORDER BY id', (quiz_id,))
    if not questions:
        return jsonify({'error': 'Quiz not found'}), 404

    question_map = {question['id']: question for question in questions}
    result_rows = []
    score = 0

    for answer in answers:
        question_id = answer.get('question_id')
        selected_index = answer.get('selected_index')
        question = question_map.get(question_id)
        if question is None or not isinstance(selected_index, int):
            continue

        choice_rows = query_db('SELECT text FROM choices WHERE question_id = ? ORDER BY id', (question_id,))
        choices = [choice['text'] for choice in choice_rows]
        correct_index = question['answer_index']
        is_correct = selected_index == correct_index
        if is_correct:
            score += 1

        result_rows.append({
            'question_id': question_id,
            'question_text': question['text'],
            'selected_index': selected_index,
            'selected_text': choices[selected_index] if 0 <= selected_index < len(choices) else None,
            'correct_index': correct_index,
            'correct_text': choices[correct_index] if 0 <= correct_index < len(choices) else None,
            'is_correct': is_correct,
            'explanation': question['explanation'],
        })

    db = get_db()
    db.execute(
        'INSERT INTO results (quiz_id, score, total, answers, created_at) VALUES (?, ?, ?, ?, ?)',
        (quiz_id, score, len(questions), json.dumps(result_rows), datetime.utcnow().isoformat()),
    )
    db.commit()

    return jsonify({
        'score': score,
        'total': len(questions),
        'details': result_rows,
    })


@app.teardown_appcontext
def teardown(exception):
    close_db(exception)


init_db()


if __name__ == '__main__':
    app.run(debug=True)
