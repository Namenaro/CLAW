
# Сценарий:
# 1. накликиваем хенд креатором точек и радиусов, добавлем их
#       как факты в генератор предсказаний. При добавлении каждого
#       факта генерим картинку среды с фактами в ХТМЛ
# 3. опять запускаем хенд креатор точек и радиусов и Н раз кликаем с радиусами.
#       Для этих областей дедаем умолчательное предсказание.
#       Резульаты окзываются в ХТМЛ логгере в следующем виде:
#      Н пар картинок, одна картинка
#      это отрисованная среда с фактами без фона  и на ней красным
#      полупрозрачным выделена область будущего предсказания.
#      Вторая картинка это картинка с одной областью предсказания.