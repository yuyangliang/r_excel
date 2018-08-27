require(plyr)
require(dplyr)
require(igraph)
require(tidyr)
require(RColorBrewer)
require(gplots)
require(ggplot2)
require(grid)
require(gridExtra)
require(ggrepel)

#Network heatmap
heatmap.2(netm, Rowv = NA, Colv = NA, col = colorRampPalette(brewer.pal(8, "Blues"))(100), key.par = list(cex = 1),
          density.info = "none", trace = 'none', keysize = 1.5, srtCol = 0, cexRow = 2, cexCol = 2)

#Plot of structure
size_prop_p = ggplot(size_prop, aes(Type, Percentage, fill = Name)) + 
  geom_bar(position = "stack",stat ="identity", width = .5) + labs(x = '') + scale_fill_brewer(palette="Set2") +
  geom_text(aes(label = Name), color = 'black', size = 7, position = position_stack(vjust = 0.5)) + 
  theme(text = element_text(size = 25), axis.text = element_text(size = 20), legend.title=element_blank(), legend.position = 'none') 

#Longitudinal plot of proportions
size_dis_p1 = ggplot(data = size_dis_2, aes(time_window, percentage, group = role, color = role)) + geom_smooth(size = 2, se = F) +
  labs(x = 'Time Window', y = 'Percentage of Role') + 
  scale_x_continuous(breaks = seq(1, 30, 4), limits = c(1, 30)) + scale_color_brewer(palette = "Set2") + 
  geom_text_repel(aes(label = label), nudge_x = .5, na.rm = T, size = 8) +
  theme(axis.title.x = element_blank(), axis.text.x = element_blank(), legend.title=element_blank(), 
        legend.position = 'none', axis.text.y = element_text(size = 20), text = element_text(size = 25))

size_dis_p2 = ggplot(data = user_num_dis, aes(time_window, num, group = 1)) + 
  geom_smooth(size = 2, color = '#778899', se = F) + 
  labs(x = 'Time Window', y = 'Number of Members') + 
  scale_x_continuous(breaks = seq(1, 30, 4), limits= c(1, 30)) +  
  theme(text = element_text(size = 25), axis.text = element_text(size = 20))

grid.newpage()
grid.draw(rbind(ggplotGrob(size_dis_p1), ggplotGrob(size_dis_p2), size = "last"))

#Cross-correlation
#Overall
ccf(nus, nsub)
#By group
apply(sub_traffic, 2, FUN = function(x){ccf(sub_us$percent_us, x, 5)})

#Plot of failure rate
#Monthly
us_nsub_p = ggplot(sub_us, aes(as.factor(time_window), scale(percent_us), group = 1, color = 'Failure rate')) + geom_smooth(size = 1.5, se = F) +
  geom_smooth(data = sub_us, aes(time_window, scale(nsub), group = 1, color = '# of questions'), size = 1.5, se = F) +
  labs(x = 'Time Window', y = 'Z-score') + scale_color_manual(values = c('#6666ff', '#66b3ff')) +
  scale_x_discrete(breaks = seq(1, 29, 4)) + 
  theme(text = element_text(size = 25), axis.text = element_text(size = 20), legend.title=element_blank(),
        legend.position = 'top')  

#Weekly
us_nsubw_p = ggplot(nsub_w, aes(as.factor(created_window), scale(percent_us), group = 1, color = 'Failure rate', linetype = 'Failure rate')) + geom_smooth(size = 1.5) +
  geom_smooth(data = nsub_w, aes(as.factor(created_window), scale(nsub), group = 1, color = '# of questions', linetype = '# of questions'), size = 1.5) +
  labs(x = 'Time Window', y = 'Z-score') + scale_color_manual(name = 'failrate', values = c('#6666ff', '#66b3ff')) + scale_linetype_manual(name = 'failrate', values = c(1, 1)) +
  theme(text = element_text(size = 25), axis.text = element_text(size = 20), legend.title=element_blank(),
        legend.position = 'top', axis.text.x=element_blank())  




