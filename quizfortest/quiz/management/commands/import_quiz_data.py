import requests
from django.core.management.base import BaseCommand
from quiz.models import Question, Choice

class Command(BaseCommand):
    help = 'Imports quiz questions from orangeoasis.pp.ua'

    def handle(self, *args, **kwargs):
        url = 'https://orangeoasis.pp.ua/questions?pm01_amount=0&pm02_amount=196'
        self.stdout.write(self.style.SUCCESS(f'Fetching data from {url}...'))
        
        response = requests.get(url)
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR('Failed to fetch data'))
            return
            
        data = response.json()
        
        # Clear existing data to avoid duplicates if run multiple times
        Question.objects.all().delete()
        
        pm02_questions = data.get('pm02', [])
        count = 0
        for item in pm02_questions:
            q_text = item.get('question')
            options = item.get('options', [])
            answer = item.get('answer')
            
            question = Question.objects.create(text=q_text, category='pm02')
            
            for opt in options:
                is_correct = (opt == answer)
                Choice.objects.create(
                    question=question,
                    text=opt,
                    is_correct=is_correct
                )
            count += 1
            
        self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} questions!'))
