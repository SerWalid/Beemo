from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/PageOff')
def PageOff():
    return render_template('PageOff.html')

@main_bp.route('/Games')
def Games():
    return render_template('Games.html')

@main_bp.route('/painting')
def painting():
    return render_template('painting.html')

@main_bp.route('/Number')
def Number():
    return render_template('Number.html')

@main_bp.route('/MemoryGame')
def MemoryGame():
    return render_template('MemoryGame.html')

@main_bp.route('/emotion')
def emotion():
    return render_template('emotion.html')

@main_bp.route('/chatbotinterface')
def chatbotinterface():
    return render_template('ChatBotInterface.html')

@main_bp.route('/EmotionDetection')
def EmotionDetection():
    return render_template('EmotionDetection.html')

@main_bp.route('/ActivitiesMenu')
def ActivitiesMenu():
    return render_template('ActivitiesMenu.html')

@main_bp.route('/Tetris')
def Tetris():
    return render_template('Tetris.html')

@main_bp.route('/Cube')
def Cube():
    return render_template('Cube.html')

@main_bp.route('/GameSelectTest')
def GameSelectTest():
    return render_template('GameSelectTest.html')

@main_bp.route('/StoryTelling')
def StoryTelling():
    return render_template('StoryTelling.html')

@main_bp.route('/chatbottest_page')
def chatbottest_page():
    return render_template('chatbotTest.html')

@main_bp.route('/Music')
def Music():
    return render_template('Music.html')

@main_bp.route('/PlayStation')
def PlayStation():
    return render_template('PlayStation.html')

@main_bp.route('/BoxCube')
def BoxCube():
    return render_template('BoxCube.html')

@main_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/beemo')
def beemo():
    return render_template('beemo.html')

@main_bp.route('/christmas')
def christmas():
    return render_template('christmas.html')

@main_bp.route('/Campfire')
def Campfire():
    return render_template('Campfire.html')

@main_bp.route('/RelaxMenu')
def RelaxMenu():
    return render_template('RelaxMenu.html')

@main_bp.route('/sidebar')
def sidebar():
    return render_template('sidebar.html')

@main_bp.route('/test')
def Test():
    return render_template('test.html')
@main_bp.route('/home')
def Home():
    return render_template('homePage.html')
@main_bp.route('/story-time')
def Story():
    return render_template('storyTime.html')