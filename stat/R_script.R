# POZOR - při každém běhu skriptu dojde k náhodnému výběru trénovacího a testovacího
# souboru, což má vliv i na trénování neuronové síě v pythonu - ten používá
# *.csv soubory vygenerované tímto skriptem. Prozatím je opakovatelnost výsledku 
# zajištěna příkazem set.seed (inicializace pokaždé stejného "náhodného" čísla.)

# Načtení a spojení dat z laboratoře a platformy

tab_lab<-read.csv2(file = "tab_lab.csv",dec = ".")
names(tab_lab)[1]<-"var"
tab_lab$id<-paste0(tab_lab$var,tab_lab$plant,tab_lab$leaf)

tab_plat<-read.csv2(dec = ".",file = "no_outliers.csv")
names(tab_plat)[1]<-"var"
tab_plat$id<-paste0(tab_plat$var,tab_plat$plant,tab_plat$leaf)

library(dplyr)

tab_plat<-tab_plat %>%
  group_by(id) %>%
  summarize_at(names(tab_plat)[5:22],.funs = "mean")

tab<-merge(x = tab_lab,y=tab_plat,by = "id")


# Příprava tesovacích a trénovacéích dat pro ANN ----

library(dplyr)

set.seed(8768) #  Pro konzistenci výsledků

train<-sample_n(tab,50)
test<-subset(tab,!(tab$id %in% train$id))

train<-train[,6:23]
test<-test[,6:23]

# Standardizace - v současné verzi vypnuta, všehny prediktory mají velmi podobné rozsahy

#library(caret)

# preproc1 <- preProcess(train[,2:18], method=c("center", "scale"))
# train<-cbind(train$spad,predict(preproc1, train[,2:18]))
# 
# preproc2 <- preProcess(test[,2:18], method=c("center", "scale"))
# test <- cbind(test$spad,predict(preproc1, test[,2:18]))
# 
# rm(preproc1,preproc2)

# Export dat

write.csv(x = train,file = "train.csv",quote = F)
write.csv(x = test,file = "test.csv",quote = F)


# LM - plný souor dat ----

step(lm(data=tab,formula=spad~r+g+b+R+G+B+mean_rgb+ExG+ExG_n+honza_1+vasek_1+kawa+yuzhu+adam+perez+geor+nas))


m<-lm(data = tab,formula = spad~G+kawa+R)
summary(m)

#----------Možnost zobrazení diagnostických grafů modelu ----

#hist(resid(m))  # histogram reziduí

#par(mfrow=c(2,3)) 
#plot(m,which=1:6) # klasická diagnostika modelu v moderním pojetí, já toto až na výjimky moc nepoužívám

# LM train/test ----

m_train<-lm(data = train,formula = spad~G+kawa+R)
summary(m_train)

test$lm_pred<-m_train$coefficients[1]+m_train$coefficients[2]*test$G+m_train$coefficients[3]*test$kawa+m_train$coefficients[4]*test$R

print(paste("Prumerna absolutni odchylka testovacich dat:",mean(abs(test$lm_pred-test$spad))))

