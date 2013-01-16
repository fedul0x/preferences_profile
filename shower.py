# -*- coding: utf-8 -*-

import web

urls = (
    '/', 'index'
)

render = web.template.render('templates/')

class index:
    def GET(self):
      db = web.database(host='db.fedul0x', dbn='postgres', 
        user='postgres', pw='postgres', db='preferences_profile')
      # profiles_types = db.select('profiles_type')
      profiles_types = db.query('SELECT * FROM profiles_type ORDER BY id;')
      comb_of_combs = []
      for r in profiles_types:
        if r.state != 'ok':
          continue
        comb_of_comb = db.query('''SELECT * FROM combination_of_combination_of_alternative_distribution
         WHERE state='ok' and profiles_type_id=%s ORDER BY id;''' % (r.id, ))
        if len(comb_of_comb)>0:
          comb_of_combs.append((comb_of_comb, len(comb_of_comb), '%sx%s' % (r.dimension_n, r.dimension_m)))
          # comb_of_combs.append((comb_of_comb, len(comb_of_comb)))
      profiles_types = db.query('SELECT * FROM profiles_type ORDER BY id;')
      return render.index(profiles_types, comb_of_combs)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

