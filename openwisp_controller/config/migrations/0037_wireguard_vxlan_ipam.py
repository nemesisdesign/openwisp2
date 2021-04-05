import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import swapper
from django.db import migrations, models

import openwisp_controller.config.base.template


class Migration(migrations.Migration):

    dependencies = [
        swapper.dependency('pki', 'Ca'),
        swapper.dependency('openwisp_ipam', 'IpAddress'),
        swapper.dependency('openwisp_ipam', 'Subnet'),
        ('config', '0036_vpn_subnet'),
    ]

    operations = [
        migrations.AddField(
            model_name='vpn',
            name='ip',
            field=models.ForeignKey(
                blank=True,
                help_text=(
                    'Internal IP address of the VPN server interface, if applicable'
                ),
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=swapper.get_model_name('openwisp_ipam', 'IpAddress'),
                verbose_name='Internal IP',
            ),
        ),
        migrations.AddField(
            model_name='vpn',
            name='private_key',
            field=models.CharField(blank=True, max_length=44),
        ),
        migrations.AddField(
            model_name='vpn',
            name='public_key',
            field=models.CharField(blank=True, max_length=44),
        ),
        migrations.AddField(
            model_name='vpn',
            name='subnet',
            field=models.ForeignKey(
                blank=True,
                help_text='Subnet IP addresses used by VPN clients, if applicable',
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=swapper.get_model_name('openwisp_ipam', 'Subnet'),
                verbose_name='Subnet',
            ),
        ),
        migrations.AddField(
            model_name='vpnclient',
            name='private_key',
            field=models.CharField(blank=True, max_length=44),
        ),
        migrations.AddField(
            model_name='vpnclient',
            name='public_key',
            field=models.CharField(blank=True, max_length=44),
        ),
        migrations.AddField(
            model_name='vpnclient',
            name='vni',
            field=models.PositiveIntegerField(
                blank=True,
                db_index=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(16777216),
                ],
            ),
        ),
        migrations.AlterField(
            model_name='template',
            name='auto_cert',
            field=models.BooleanField(
                db_index=True,
                default=openwisp_controller.config.base.template.default_auto_cert,
                help_text=(
                    'whether tunnel specific configuration (cryptographic keys, '
                    'ip addresses, etc) should be automatically generated and '
                    'managed behind the scenes for each configuration using this '
                    'template, valid only for the VPN type'
                ),
                verbose_name='automatic tunnel provisioning',
            ),
        ),
        migrations.AlterField(
            model_name='vpn',
            name='ca',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=swapper.get_model_name('pki', 'Ca'),
                verbose_name='Certification Authority',
            ),
        ),
        migrations.AlterUniqueTogether(
            name='vpnclient', unique_together={('config', 'vpn'), ('vpn', 'vni')},
        ),
        migrations.AddField(
            model_name='vpnclient',
            name='ip',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=swapper.get_model_name('openwisp_ipam', 'IpAddress'),
            ),
        ),
    ]
