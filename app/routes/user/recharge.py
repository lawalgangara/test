from app import app, db 
from flask import render_template, redirect, request, flash, url_for, session
from app.models.user import User, Transaction



@app.route('/recharge', methods=['GET', 'POST'])
def recharge():

     # Retrieve user_id from session
     user_id = session.get('user_id')
     if user_id:
          user = User.query.get(user_id)

          if request.method == 'POST':
               amount = float(request.form['amount'])

               # Calculate the discount amount(10% of the recharge)
               discount = amount * 0.1
               total_amount = amount - discount

               # Check if the user has sufficient balance
               if total_amount > user.balance:
                    flash('Insufficient balance', 'danger')
                    return redirect(url_for('recharge'))
               # Update the user's balance
               user.balance -= total_amount

               # Update the database
               db.session.commit()

               transaction = Transaction(
                    user_id=user.id,
                    recipient_name=user.full_name,
                    recipient_card_number=user.card_number,
                    amount=total_amount,
                    type="Debit - Airtime Purchase"

               )

               db.session.add(transaction)
               db.session.commit()

               return render_template('user/recharge_success.html', amount=total_amount, discount=discount)
          return render_template('user/recharge.html', user=user)
     else:
          flash('You need to be logged in first', 'danger')
          return redirect(url_for('login'))
