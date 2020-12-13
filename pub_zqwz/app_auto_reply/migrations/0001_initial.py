# Generated by Django 2.2.3 on 2020-12-05 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='pubKeys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=200, unique=True)),
                ('key_info', models.CharField(max_length=2000)),
            ],
            options={
                'db_table': 'pub_keys',
            },
        ),
        migrations.CreateModel(
            name='pubVarList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('var_name', models.CharField(max_length=20, unique=True)),
                ('var_info', models.CharField(max_length=2000)),
                ('note', models.CharField(max_length=100, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'pub_var_list',
            },
        ),
        migrations.CreateModel(
            name='pubWZEquip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cx_name', models.CharField(max_length=200)),
                ('cx_value', models.CharField(max_length=5000)),
                ('cx_value1', models.CharField(max_length=5000)),
                ('hero_name', models.CharField(max_length=20)),
                ('hero_id', models.IntegerField()),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'pub_wz_equip',
            },
        ),
        migrations.CreateModel(
            name='pubWZHeroName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hero_id', models.IntegerField()),
                ('hero_name', models.CharField(max_length=20)),
                ('hero_name_bm', models.CharField(max_length=20, null=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'pub_wz_hero_name',
            },
        ),
        migrations.CreateModel(
            name='pubWZIntroduce',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cx_name', models.CharField(max_length=200)),
                ('cx_value', models.CharField(max_length=5000)),
                ('hero_name', models.CharField(max_length=20)),
                ('hero_id', models.IntegerField()),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'pub_wz_introduce',
            },
        ),
        migrations.CreateModel(
            name='pubWZKZ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cx_name', models.CharField(max_length=200)),
                ('cx_value', models.CharField(max_length=5000)),
                ('hero_name', models.CharField(max_length=20)),
                ('hero_id', models.IntegerField()),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'pub_wz_kz',
            },
        ),
        migrations.CreateModel(
            name='pubWZNews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc_id', models.CharField(max_length=50)),
                ('news_title', models.CharField(max_length=200)),
                ('news_title_url', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'pub_wz_news',
            },
        ),
        migrations.CreateModel(
            name='pubWZRune',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cx_name', models.CharField(max_length=200)),
                ('cx_value', models.CharField(max_length=5000)),
                ('hero_name', models.CharField(max_length=20)),
                ('hero_id', models.IntegerField()),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'pub_wz_rune',
            },
        ),
        migrations.CreateModel(
            name='pubWZSkill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cx_name', models.CharField(max_length=200)),
                ('cx_value', models.CharField(max_length=5000)),
                ('hero_name', models.CharField(max_length=20)),
                ('hero_id', models.IntegerField()),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'pub_wz_skill',
            },
        ),
        migrations.CreateModel(
            name='pubWZSkills',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cx_name', models.CharField(max_length=200)),
                ('cx_value', models.CharField(max_length=5000)),
                ('hero_name', models.CharField(max_length=20)),
                ('hero_id', models.IntegerField()),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'pub_wz_skills',
            },
        ),
        migrations.CreateModel(
            name='pubWZVoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hero_name', models.CharField(max_length=100)),
                ('voice_url', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'pub_wz_voice',
            },
        ),
        migrations.CreateModel(
            name='pubWZWall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skin_name', models.CharField(max_length=20)),
                ('skin_url', models.CharField(max_length=500)),
                ('hero_name', models.CharField(max_length=10, null=True)),
                ('hero_name_bm', models.CharField(max_length=50, null=True)),
                ('hero_id', models.IntegerField(null=True)),
                ('skin_short_url', models.CharField(max_length=100)),
                ('mob_skin_url', models.CharField(max_length=500, null=True)),
                ('mob_skin_short_url', models.CharField(max_length=100, null=True)),
            ],
            options={
                'db_table': 'pub_wz_wall',
            },
        ),
        migrations.CreateModel(
            name='pubWZwinRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cx_name', models.CharField(max_length=200)),
                ('cx_value', models.CharField(max_length=5000)),
                ('hero_name', models.CharField(max_length=20)),
                ('hero_id', models.IntegerField()),
                ('update_time_str', models.CharField(max_length=20)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'pub_wz_win_rate',
            },
        ),
        migrations.CreateModel(
            name='pubWZZH',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cx_name', models.CharField(max_length=200)),
                ('cx_value', models.CharField(max_length=5000)),
                ('hero_name', models.CharField(max_length=20)),
                ('hero_id', models.IntegerField()),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'pub_wz_zh',
            },
        ),
    ]