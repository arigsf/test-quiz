import pytest
from model import Question

def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_add_first_choice_generates_id_one():
    question = Question(title='q1')
    choice = question.add_choice('a')
    
    assert choice.id == 1

def test_add_subsequent_choice_generates_incremental_id():
    question = Question(title='q1')
    question.add_choice('a')
    choice2 = question.add_choice('b')
    
    assert choice2.id == 2

def test_add_choice_with_empty_text_raises_exception():
    question = Question(title='q1')
    
    with pytest.raises(Exception, match='Text cannot be empty'):
        question.add_choice('')

def test_add_choice_with_text_too_long_raises_exception():
    question = Question(title='q1')
    
    with pytest.raises(Exception, match='Text cannot be longer than 100 characters'):
        question.add_choice('a' * 101)

def test_remove_existing_choice_decreases_list_size():
    question = Question(title='q1')
    choice1 = question.add_choice('a')
    question.add_choice('b')
    
    question.remove_choice_by_id(choice1.id)
    
    assert len(question.choices) == 1

def test_correct_selected_choices_exceeding_max_selections_raises_exception():
    question = Question(title='q1', max_selections=1)
    choice1 = question.add_choice('a')
    choice2 = question.add_choice('b')
    
    with pytest.raises(Exception, match='Cannot select more than 1 choices'):
        question.correct_selected_choices([choice1.id, choice2.id])

def test_remove_nonexistent_choice_raises_exception():
    question = Question(title='q1')
    question.add_choice('a')
    
    with pytest.raises(Exception, match='Invalid choice id'):
        question.remove_choice_by_id(999)

def test_remove_all_choices_clears_the_list():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    
    question.remove_all_choices()
    
    assert len(question.choices) == 0

def test_set_correct_choices_updates_is_correct_flag():
    question = Question(title='q1')
    choice = question.add_choice('a')
    
    question.set_correct_choices([choice.id])
    
    assert choice.is_correct

def test_correct_selected_choices_returns_only_correct_matches():
    question = Question(title='q1', max_selections=2)
    choice1 = question.add_choice('a', is_correct=True)
    choice2 = question.add_choice('b', is_correct=False)
    
    correct_selections = question.correct_selected_choices([choice1.id, choice2.id])
    
    assert correct_selections == [choice1.id]

@pytest.fixture
def question_with_choices():
    question = Question(title='q1', max_selections=3)
    c1 = question.add_choice('a', is_correct=True)
    c2 = question.add_choice('b', is_correct=False)
    c3 = question.add_choice('c', is_correct=True)
    return question

def test_fixture_has_three_choices(question_with_choices):
    assert len(question_with_choices.choices) == 3

def test_correct_selected_choices_with_fixture(question_with_choices):
    ids = [choice.id for choice in question_with_choices.choices]
    
    result = question_with_choices.correct_selected_choices(ids)
    
    correct_ids = [choice.id for choice in question_with_choices.choices if choice.is_correct]
    
    assert result == correct_ids