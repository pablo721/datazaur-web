# Generated by Django 4.1.3 on 2023-02-09 00:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('crypto', '0001_initial'),
        ('website', '0001_initial'),
        ('markets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Watchlist', max_length=32)),
                ('crypto_tickers', models.ManyToManyField(blank=True, related_name='watchlist_crypto_tickers', to='crypto.cryptoticker')),
                ('currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='watchlist_currency', to='markets.currency')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users_watchlists', to='website.account')),
                ('source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='watchlist_source', to='crypto.cryptoexchange')),
            ],
        ),
    ]