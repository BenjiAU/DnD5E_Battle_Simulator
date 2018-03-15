@admin.route('/combatant/create', methods = ['GET', 'POST'])
def create_combatnat():
    form = CreateCombatantForm (request.form)
    if request.method == 'POST' and form.validate():
        combatant = Combatant(form.names.data)
        db.session.add(combatant)
        db.session.commit()
        flash('Combatant successfully created.')

        return redirect(url_for('main.display_authors'))

return render_template('create_author.htm', form=form)