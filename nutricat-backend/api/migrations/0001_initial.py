                                               







import django.db.models.deletion



from django.conf import settings



from django.db import migrations, models











class Migration(migrations.Migration):







    initial = True







    dependencies = [



        migrations.swappable_dependency(settings.AUTH_USER_MODEL),



    ]







    operations = [



        migrations.CreateModel(



            name='DietaryNorm',



            fields=[



                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),



                ('factor_name', models.CharField(max_length=50)),



                ('multiplier_value', models.DecimalField(decimal_places=2, max_digits=3)),



            ],



        ),



        migrations.CreateModel(



            name='FoodProduct',



            fields=[



                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),



                ('brand', models.CharField(max_length=100)),



                ('product_name', models.CharField(max_length=200)),



                ('food_type', models.CharField(max_length=20)),



                ('calories_100g', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),



                ('protein_pct', models.DecimalField(decimal_places=2, max_digits=5)),



                ('fat_pct', models.DecimalField(decimal_places=2, max_digits=5)),



                ('fiber_pct', models.DecimalField(decimal_places=2, max_digits=5)),



            ],



        ),



        migrations.CreateModel(



            name='Cat',



            fields=[



                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),



                ('name', models.CharField(max_length=50)),



                ('breed', models.CharField(blank=True, max_length=50, null=True)),



                ('gender', models.CharField(max_length=10)),



                ('birth_date', models.CharField(max_length=20)),



                ('weight_kg', models.DecimalField(decimal_places=2, max_digits=4)),



                ('body_condition', models.CharField(max_length=20)),



                ('activity_level', models.CharField(max_length=20)),



                ('is_neutered', models.BooleanField(default=False)),



                ('photo_url', models.TextField(blank=True, null=True)),



                ('description', models.TextField(blank=True, null=True)),



                ('tips', models.TextField(blank=True, null=True)),



                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cats', to=settings.AUTH_USER_MODEL)),



            ],



        ),



        migrations.CreateModel(



            name='CatRation',



            fields=[



                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),



                ('daily_portion_g', models.IntegerField()),



                ('feeding_time', models.CharField(max_length=20)),



                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rations', to='api.cat')),



                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rations', to='api.foodproduct')),



            ],



        ),



    ]



