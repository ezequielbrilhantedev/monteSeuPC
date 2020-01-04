from rest_framework.serializers import ModelSerializer, SlugRelatedField, StringRelatedField, HyperlinkedIdentityField, ValidationError
from monteseupc.models import *
import re


def validarMontagemPlacaMae(value):
	if str(value['placa_mae'].processadores_suportados) == 'ambos':
		return value
	elif str(value['processador'].marca) != str(value['placa_mae'].processadores_suportados):
		raise ValidationError("Processador não suportado pela a Placa Mãe")
	return value


def validarMemoria(value):
	total_escolhida = int(re.sub("[^0-9]", '', value['tamanho_da_memoria'])) * int(value['qtd_de_memoria'])
	tamanho_memoria = int(re.sub("[^0-9]", '', str(value['placa_mae'].memoria_suportada)))

	if total_escolhida > tamanho_memoria:
		raise ValidationError('Memória não suportada pela a placa mãe. Escolha igual ou menor a {}GB'.format(
			tamanho_memoria, total_escolhida))
	return value


def validarPlacaDeVideo(value):
	if value['placa_mae'].video_integrado == False and value['placa_de_video'] == None:
		raise ValidationError("A placa mãe não possui vídeo integrado, por favor escolha uma.")
	return value


def validarQuantidadeDeSlots(value):
	if value['qtd_memoria'] > value['placa_mae'].slots:
		raise ValidationError('Quantidade incompatível, a placa mãe so possui {} slots.'.format(value['placa_mae'].slots))
	return value



class MonteSeuPcSerializer(ModelSerializer):
	processador = SlugRelatedField(
		slug_field='produto',
		queryset=Processador.obejcts.all()
	)
	memoria = SlugRelatedField(
		slug_field='produto',
		queryset=Memoria.objects.all()
	)
	placa_mae = SlugRelatedField(
		slug_field='produto',
		queryset=PlacaMae.objects.all()
	)
	placa_de_video = SlugRelatedField(
		slug_field='produto',
		allow_null=True,
		queryset=PlacaDeVideo.objects.all()
	)

	class Meta:
		model = MonteSeuPC
		fields = [
			'id', 'processador', 'placa_mae', 'memoria', 'qtd_memoria', 'tamanho_da_memoria', 'placa_de_video'
		]