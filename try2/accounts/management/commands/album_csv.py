import csv
from datetime import datetime
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import transaction
from accounts.models import Album, Review, Aoty

def safe_get_decimal(value, default=Decimal('0.0')):
    try:
        return Decimal(value)
    except decimal.InvalidOperation as e:
        print(f"Error converting {value} to Decimal: {e}")
        return default

def safe_get_int(value, default=0):
    try:
        return int(value)
    except ValueError as e:
        print(f"Error converting {value} to int: {e}")
        return default

errors = []  # List to store error messages

with open('accounts/account_data/album_ratings.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            required_fields = [
                'Release Year', 'Release Month', 'Release Day', 
                'Artist', 'Title', 'Format', 'Label', 'Genre'
            ]
            missing_fields = [field for field in required_fields if field not in row or not row[field].strip()]
            if missing_fields:
                raise ValidationError(f"Missing data for fields: {', '.join(missing_fields)}")

            # Format release date
            release_date_str = f"{row['Release Year']}-{row['Release Month']}-{row['Release Day']}"
            release_date = datetime.strptime(release_date_str, '%Y-%B-%d')

            # Using transaction.atomic to ensure all or nothing
            with transaction.atomic():
                # Get or create album
                album, created = Album.objects.get_or_create(
                    artist=row['Artist'],
                    title=row['Title'],
                    defaults={
                        'release_date': release_date,
                        'format': row['Format'],
                        'label': row['Label'],
                        'genre': row['Genre'],
                    }
                )
                
                # Create Review record
                Review.objects.create(
                    album=album,
                    metacritic_critic_score=safe_get_decimal(row.get('Metacritic Critic Score')),
                    metacritic_reviews=safe_get_int(row.get('Metacritic Reviews')),
                    metacritic_user_score=safe_get_decimal(row.get('Metacritic User Score')),
                    metacritic_user_reviews=safe_get_int(row.get('Metacritic User Reviews'))
                )
                
                # Create Aoty record
                Aoty.objects.create(
                    album=album,
                    aoty_critic_score=safe_get_decimal(row.get('AOTY Critic Score')),
                    aoty_critic_reviews=safe_get_int(row.get('AOTY Critic Reviews')),
                    aoty_user_score=safe_get_decimal(row.get('AOTY User Score')),
                    aoty_user_reviews=safe_get_int(row.get('AOTY User Reviews'))
                )
        except Exception as e:
            error_message = f"Error processing row {reader.line_num}: {e}"
            print(error_message)
            errors.append(error_message)  # Append error to the list

# Optionally, save or process the collected errors further
if errors:
    with open('errors_log.txt', 'w') as f:
        for error in errors:
            f.write(f"{error}\n")
