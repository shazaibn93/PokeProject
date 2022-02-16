from. import bp as main
from flask import render_template, request, flash, redirect,url_for
import requests
from .forms import PokeForm
from flask_login import login_required, current_user, logout_user
from app.models import Poketeam, User, Caughtem

@main.route('/', methods=['GET'])
def index():
    return render_template('index.html.j2')

@main.route('/team', methods=['GET','POST'])
def team():
    form=PokeForm()
    if request.method == 'POST' and form.validate_on_submit():
        # contact the api and get the name of the pokemon from the form
        poke = request.form.get('poke').lower()
        url = f"https://pokeapi.co/api/v2/pokemon/{poke}"
        response = requests.get(url)
        if response.ok:
            poke_dict={
                'name':response.json()['forms'][0]['name'],
                 "hp":response.json()['stats'][0]['base_stat'],
                "defense":response.json()['stats'][2]['base_stat'],
                "attack":response.json()['stats'][1]['base_stat'],
                "ability_1":response.json()['abilities'][0]['ability']['name'],
                "ability_2":response.json()['abilities'][1]['ability']['name'],
                "sprite": response.json()['sprites']['front_shiny']
            }

            if not Poketeam.exists(poke_dict['name']):
                pokem = Poketeam()
                pokem.from_dict(poke_dict)
                pokem.save()

            user = current_user
            # if user.inteam(poke_dict):
            #     pass
            # else:
            user.add_to_team(Poketeam.exists(poke_dict['name']))

            return render_template('team.html.j2', form=form, mpoke = poke_dict )

        else:
            error_string = "Houston We Have a Problem"
            return render_template('team.html.j2', form=form, error = error_string)
    return render_template('team.html.j2', form=form)

@main.route('/my_squad', methods=['GET'])
def my_squad():
    team = current_user.squad
    return render_template('my_squad.html.j2', team=team)

@main.route('/delete/<int:id>', methods=['GET'])
def remove(id):
    deleted = Caughtem.query.get((id,current_user.id))
    deleted.delete()
    flash(f'You have removed pokemon from the squad, they will be missed', 'warning')
    return redirect(url_for('main.my_squad'))


