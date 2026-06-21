from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Choice
import random

def index(request):
    if request.method == 'POST':
        # Start new quiz with original order
        questions = list(Question.objects.order_by('id').values_list('id', flat=True))
        # Include all questions instead of limiting
        request.session['quiz_questions'] = questions
        request.session['current_index'] = 0
        request.session['score'] = 0
        request.session['answers'] = [] # To store user answers for review
        return redirect('quiz:question')
    return render(request, 'quiz/index.html')

def question_view(request):
    questions = request.session.get('quiz_questions', [])
    current_index = request.session.get('current_index', 0)
    
    if current_index >= len(questions):
        return redirect('quiz:result')
        
    question_id = questions[current_index]
    question = get_object_or_404(Question, id=question_id)
    choices = question.choices.all().order_by('id') # Or randomize choices?
    
    # Map choices to A, B, C, D, E
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    choice_data = []
    for i, choice in enumerate(choices):
        choice_data.append({
            'letter': letters[i] if i < len(letters) else str(i+1),
            'obj': choice
        })
        
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'stop':
            return redirect('quiz:result')
            
        selected_choice_id = request.POST.get('choice')
        if selected_choice_id:
            selected_choice = get_object_or_404(Choice, id=selected_choice_id)
            is_correct = selected_choice.is_correct
            
            if is_correct:
                request.session['score'] += 1
                
            request.session['answers'].append({
                'question': question.text,
                'selected': selected_choice.text,
                'is_correct': is_correct,
                'correct_answer': question.choices.filter(is_correct=True).first().text
            })
            
            request.session['current_index'] += 1
            request.session.modified = True
            return redirect('quiz:question')
            
    # Find the correct choice ID for JS to reveal
    correct_choice = question.choices.filter(is_correct=True).first()
            
    context = {
        'question': question,
        'choices': choice_data,
        'current_number': current_index + 1,
        'total': len(questions),
        'correct_choice_id': correct_choice.id if correct_choice else None,
    }
    return render(request, 'quiz/question.html', context)

def result_view(request):
    score = request.session.get('score', 0)
    total = len(request.session.get('quiz_questions', []))
    answers = request.session.get('answers', [])
    
    context = {
        'score': score,
        'total': total,
        'answers': answers,
    }
    return render(request, 'quiz/result.html', context)
